from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlalchemy.types import TypeDecorator
from sqlmodel import SQLModel, Field, create_engine

from workflow import State, Action, Role


class UTCDateTime(TypeDecorator):
    """Store UTC, and always hand back timezone-aware UTC.

    SQLite drops timezone info, so without this the API would return times with
    no offset and the browser would read them as local time.
    """
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None and value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        return value.replace(tzinfo=timezone.utc) if value is not None else None


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    applicant_name: str
    village: str
    declared_income: int
    occupation: str = ""
    family_members: int = 0
    documents: str = ""
    status: State = State.SUBMITTED
    created_at: datetime = Field(default_factory=utcnow, sa_column=Column(UTCDateTime()))
    # When the case reached its current stage. Urgency is measured from here,
    # not from submission, so it shows who is holding the case up right now.
    stage_entered_at: datetime = Field(default_factory=utcnow, sa_column=Column(UTCDateTime()))


class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    from_state: str
    to_state: str
    action: Action
    role: Role
    actor_name: str
    reason: str = Field(default="")
    # How the officer used the AI draft reason: "none", "used" (as is) or "edited".
    # This is what makes an "AI override rate" measurable.
    ai_reason_use: str = Field(default="none")
    created_at: datetime = Field(default_factory=utcnow, sa_column=Column(UTCDateTime()))


engine = create_engine("sqlite:///app.db")


def create_db():
    SQLModel.metadata.create_all(engine)
