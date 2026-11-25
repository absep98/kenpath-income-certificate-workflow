from enum import Enum

class State(str, Enum):
    SUBMITTED = "submitted"
    FIELD_VERIFICATION = "field_verification"
    RI_REVIEW = "ri_review"
    FINAL_DECISION = "final_decision"
    APPROVED = "approved"
    REJECTED = "rejected"

class Role(str, Enum):
    VILLAGE_ACCOUNTANT = "village_accountant"
    REVENUE_INSPECTOR = "revenue_inspector"
    TAHSILDAR = "tahsildar"

class Action(str, Enum):
    FORWARD = "forward"
    RETURN_ = "return"
    REJECT = "reject"
    APPROVE = "approve"

TRANSITIONS = {
    (State.SUBMITTED, Action.FORWARD, Role.VILLAGE_ACCOUNTANT): State.FIELD_VERIFICATION,
    (State.SUBMITTED, Action.REJECT, Role.VILLAGE_ACCOUNTANT): State.REJECTED,
    (State.FIELD_VERIFICATION, Action.FORWARD, Role.VILLAGE_ACCOUNTANT): State.RI_REVIEW,
    (State.FIELD_VERIFICATION, Action.RETURN_, Role.VILLAGE_ACCOUNTANT): State.SUBMITTED,
    (State.FIELD_VERIFICATION, Action.REJECT, Role.VILLAGE_ACCOUNTANT): State.REJECTED,
    (State.RI_REVIEW, Action.FORWARD, Role.REVENUE_INSPECTOR): State.FINAL_DECISION,
    (State.RI_REVIEW, Action.RETURN_, Role.REVENUE_INSPECTOR): State.FIELD_VERIFICATION,
    (State.RI_REVIEW, Action.REJECT, Role.REVENUE_INSPECTOR): State.REJECTED,
    (State.FINAL_DECISION, Action.APPROVE, Role.TAHSILDAR): State.APPROVED,
    (State.FINAL_DECISION, Action.REJECT, Role.TAHSILDAR): State.REJECTED,
    (State.FINAL_DECISION, Action.RETURN_, Role.TAHSILDAR): State.RI_REVIEW,
}

class InvalidTransition(Exception):
    pass


def next_state(state, action, role):
    key = (state, action, role)
    if key not in TRANSITIONS:
        raise InvalidTransition(f"{role.value} cannot {action.value} when {state.value}")
    return TRANSITIONS[key]

def states_for_role(role):
    return {key[0] for key in TRANSITIONS if key[2] == role}


def allowed_actions(state, role):
    return {key[1] for key in TRANSITIONS if key[0] == state and key[2] == role}