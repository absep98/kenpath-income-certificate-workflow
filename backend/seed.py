"""Seed demo data: Kannada applications spread across the workflow.

Run from the backend folder:  .venv\\Scripts\\python.exe seed.py

WARNING: this drops and recreates all tables. Demo use only.
"""
from datetime import datetime, timedelta, timezone

from sqlmodel import SQLModel, Session

from auth import USERS
from models import Application, engine
from services import perform_action
from workflow import Action, Role

VA, RI = Role.VILLAGE_ACCOUNTANT, Role.REVENUE_INSPECTOR
FWD, RET = Action.FORWARD, Action.RETURN_

# role -> display name of the demo officer, taken from auth.USERS
ACTOR = {u["role"]: u["name"] for u in USERS.values()}

ALL_DOCS = "aadhaar,ration_card,income_affidavit,photo"

# Each path is a list of (action, role, reason). Walking it with perform_action
# leaves the application in the right state with a real history trail.
TO_FIELD = [(FWD, VA, "ಅರ್ಜಿ ಸ್ವೀಕರಿಸಲಾಗಿದೆ")]
TO_RI = TO_FIELD + [(FWD, VA, "ಸ್ಥಳ ಪರಿಶೀಲನೆ ಪೂರ್ಣಗೊಂಡಿದೆ")]
TO_FINAL = TO_RI + [(FWD, RI, "ದಾಖಲೆಗಳು ಹೊಂದಾಣಿಕೆಯಾಗಿವೆ")]
RETURNED = TO_RI + [(RET, RI, "ಆದಾಯ ಘೋಷಣೆ ಸ್ಪಷ್ಟವಿಲ್ಲ, ಮತ್ತೊಮ್ಮೆ ಪರಿಶೀಲಿಸಿ")]

# (name, village, income, occupation, family, documents, days_old, days_at_stage, path)
CASES = [
    # Waiting for the Village Accountant (new)
    ("ರಾಜೇಶ್ ಕುಮಾರ್", "ಹೆಬ್ಬಾಳ", 85000, "ಕೃಷಿ ಕೂಲಿ", 5, ALL_DOCS, 9, 9, []),
    ("ಲಕ್ಷ್ಮಿ ದೇವಿ", "ಯಲಹಂಕ", 60000, "ದಿನಗೂಲಿ", 4, "aadhaar,photo", 2, 2, []),
    # In field verification (Village Accountant)
    ("ಮಂಜುನಾಥ್ ಗೌಡ", "ದೊಡ್ಡಬಳ್ಳಾಪುರ", 120000, "ಚಿಕ್ಕ ಅಂಗಡಿ", 4, ALL_DOCS, 12, 6, TO_FIELD),
    ("ಸುಮಿತ್ರಾ ಬಾಯಿ", "ನೆಲಮಂಗಲ", 900000, "ದಿನಗೂಲಿ", 3, ALL_DOCS, 5, 3, TO_FIELD),
    ("ಶಿವಕುಮಾರ್", "ಹೊಸಕೋಟೆ", 95000, "ಆಟೋ ಚಾಲಕ", 5, ALL_DOCS, 3, 1, RETURNED),
    # In RI review
    ("ಅನಿತಾ ಎಸ್", "ಹೆಬ್ಬಾಳ", 70000, "ಟೈಲರ್", 3, ALL_DOCS, 7, 2, TO_RI),
    # Waiting for the Tahsildar
    ("ರಮೇಶ್ ನಾಯ್ಕ್", "ಯಲಹಂಕ", 110000, "ಕೃಷಿ", 6, ALL_DOCS, 10, 4, TO_FINAL),
    ("ಗೀತಾ ಹೆಗಡೆ", "ನೆಲಮಂಗಲ", 80000, "ಟೈಲರ್", 4, ALL_DOCS, 4, 1, TO_FINAL),
]


def seed():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        for name, village, income, occupation, family, docs, days_old, days_at_stage, path in CASES:
            application = Application(
                applicant_name=name,
                village=village,
                declared_income=income,
                occupation=occupation,
                family_members=family,
                documents=docs,
                created_at=datetime.now(timezone.utc) - timedelta(days=days_old),
            )
            session.add(application)
            session.commit()
            session.refresh(application)
            for action, role, reason in path:
                perform_action(session, application.id, action, role, ACTOR[role], reason)
            # Back-date the stage entry so the queue shows realistic waiting times.
            application.stage_entered_at = datetime.now(timezone.utc) - timedelta(days=days_at_stage)
            session.add(application)
            session.commit()
    print(f"Seeded {len(CASES)} applications.")


if __name__ == "__main__":
    seed()
