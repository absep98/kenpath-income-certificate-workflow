import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from models import Application, History
from workflow import State, Role, Action, InvalidTransition
from services import perform_action, ReasonRequired

# a fixture is resuable setup code that provides resources to tests
@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_forward_updates_status_and_writes_history(session):
    app = Application(
        applicant_name="Aks",
        village="Kathua",
        declared_income=90000,
        status=State.FIELD_VERIFICATION
    )

    session.add(app)
    session.commit()

    perform_action(session, app.id, Action.FORWARD, Role.VILLAGE_ACCOUNTANT, "AKS Sharma")

    assert app.status == State.RI_REVIEW
    rows = session.exec(select(History)).all()
    assert len(rows) == 1
    assert rows[0].from_state == "field_verification"
    assert rows[0].to_state == "ri_review"


def test_forward_negative_updates(session):
    app = Application(
        applicant_name="Aks",
        village="Kathua",
        declared_income=90000,
        status=State.FIELD_VERIFICATION
    )

    session.add(app)
    session.commit()

    with pytest.raises(InvalidTransition):
        perform_action(session, app.id, Action.FORWARD, Role.REVENUE_INSPECTOR, "Vanshu Sharma")

    assert app.status == State.FIELD_VERIFICATION
    rows = session.exec(select(History)).all()
    assert len(rows) == 0

def test_return_without_reason_is_refused_and_changes_nothing(session):
    app = Application(
        applicant_name="Aks",
        village="Kathua",
        declared_income=90000,
        status=State.RI_REVIEW
    )
    session.add(app)
    session.commit()

    for blank in ("", "   "):
        with pytest.raises(ReasonRequired):
            perform_action(session, app.id, Action.RETURN_, Role.REVENUE_INSPECTOR, "Meena", blank)

    assert app.status == State.RI_REVIEW
    assert len(session.exec(select(History)).all()) == 0

    perform_action(session, app.id, Action.RETURN_, Role.REVENUE_INSPECTOR, "Meena", "Income unclear")
    assert app.status == State.FIELD_VERIFICATION


def test_action_records_stage_entry_time_and_ai_use(session):
    app = Application(
        applicant_name="Aks",
        village="Kathua",
        declared_income=90000,
        status=State.FIELD_VERIFICATION
    )
    session.add(app)
    session.commit()
    before = app.stage_entered_at

    perform_action(session, app.id, Action.FORWARD, Role.VILLAGE_ACCOUNTANT, "Suresh", "ok", "edited")

    assert app.stage_entered_at >= before
    row = session.exec(select(History)).all()[0]
    assert row.ai_reason_use == "edited"


def test_failed_commit_rolls_back_status_and_history(session, monkeypatch):
    app = Application(
        applicant_name="Aks",
        village="Kathua",
        declared_income=90000,
        status=State.FIELD_VERIFICATION
    )
    session.add(app)
    session.commit()

    def broken_commit():
        raise RuntimeError("database went away")

    monkeypatch.setattr(session, "commit", broken_commit)
    with pytest.raises(RuntimeError):
        perform_action(session, app.id, Action.FORWARD, Role.VILLAGE_ACCOUNTANT, "Suresh")
    monkeypatch.undo()

    session.refresh(app)
    assert app.status == State.FIELD_VERIFICATION
    assert len(session.exec(select(History)).all()) == 0
