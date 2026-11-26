import os
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from auth import USERS, create_token, current_user
from models import Application, engine, create_db, History
from workflow import states_for_role, Action, InvalidTransition, allowed_actions
from services import perform_action, ReasonRequired
from ai import rule_flags, flag_text, llm_assist, document_status

create_db()
# Demo hosting has an ephemeral disk: if the database is empty, load the demo cases.
# Demo-only behaviour: set DEMO_SEED=0 to disable it (e.g. for any real deployment).
if os.environ.get("DEMO_SEED", "1") != "0":
    with Session(engine) as _s:
        if _s.exec(select(Application)).first() is None:
            from seed import seed
            seed()
app = FastAPI(title="Workflow API")


def get_session():
    with Session(engine) as session:
        yield session


class LoginIn(BaseModel):
    username: str
    password: str

class ActionIn(BaseModel):
    action: Action
    reason: str = Field(default="", max_length=1000)
    # "none", "used" or "edited": how the officer used the AI draft reason (for impact metrics).
    ai_reason_use: str = "none"


@app.post("/login")
def login(body: LoginIn):
    user = USERS.get(body.username)
    if user is None or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return {"token": create_token(body.username), "name": user["name"], "role": user["role"].value}


@app.get("/applications")
def list_applications(
        lang: str = "kn",
        user=Depends(current_user),
        session: Session = Depends(get_session)
    ):
    """The officer's queue. Longest time at the CURRENT stage first, with rule flags per case."""
    states = states_for_role(user["role"])
    query = select(Application).where(Application.status.in_(states)).order_by(Application.stage_entered_at)
    return [
        {**a.model_dump(mode="json"), "flags": [flag_text(c, lang) for c in rule_flags(a)]}
        for a in session.exec(query).all()
    ]


@app.post("/applications/{application_id}/action")
def take_action(
        application_id: int,
        body: ActionIn,
        user=Depends(current_user),
        session: Session=Depends(get_session)
    ):
    try:
        application = perform_action(session, application_id, body.action, user["role"], user["name"], body.reason, body.ai_reason_use)

    except InvalidTransition as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ReasonRequired as e:
        raise HTTPException(status_code=422, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return application


@app.get("/applications/{application_id}")
def get_applications(
        application_id: int,
        lang: str = "kn",
        user=Depends(current_user),
        session: Session = Depends(get_session)
    ):
    application = session.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    query = select(History).where(History.application_id == application_id).order_by(History.created_at)
    history = session.exec(query).all()

    # An officer may open a case that is at their stage, or one they have already acted on.
    mine = application.status in states_for_role(user["role"]) or any(h.role == user["role"] for h in history)
    if not mine:
        raise HTTPException(status_code=403, detail="This case is not assigned to your role")

    actions = [a.value for a in allowed_actions(application.status, user["role"])]
    return {
        "application": application,
        "documents": document_status(application, lang),
        "history": history,
        "allowed_actions": actions,
    }


@app.post("/applications/{application_id}/assist")
def assist(
        application_id: int,
        lang: str = "kn",
        user=Depends(current_user),
        session: Session = Depends(get_session)
    ):
    """AI suggestion only. Rule flags always work; the LLM part is optional."""
    application = session.get(Application, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.status not in states_for_role(user["role"]):
        raise HTTPException(status_code=403, detail="Not your case at this stage")

    history = session.exec(
        select(History).where(History.application_id == application_id).order_by(History.created_at)
    ).all()
    codes = rule_flags(application)
    llm = llm_assist(application, history, codes, lang)
    return {
        "flags": [flag_text(c, lang) for c in codes],
        "summary": llm["summary"] if llm else "",
        "suggested_reason": llm["suggested_reason"] if llm else "",
    }


# Serve the frontend. Mounted LAST so the API routes above take priority.
app.mount("/", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="static")
