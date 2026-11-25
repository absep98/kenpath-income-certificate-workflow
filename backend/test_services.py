import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from models import Application, History
from workflow import State, Role, Action, InvalidTransition
from services import perform_action

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