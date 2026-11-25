from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine
from workflow import State, Action, Role


class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    applicant_name: str
    village: str
    declared_income: int
    occupation: str = ""
    family_members: int = 0
    documents: str = ""
    status: State = State.SUBMITTED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    from_state: str
    to_state: str
    action: Action
    role: Role
    actor_name: str
    reason: str = Field(default="")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

engine = create_engine("sqlite:///app.db")

def create_db():
    SQLModel.metadata.create_all(engine)