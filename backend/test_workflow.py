import pytest
from workflow import State, Role, Action, next_state, InvalidTransition, states_for_role, allowed_actions
from itertools import product

def test_va_can_forward_field_verification():
    result = next_state(State.FIELD_VERIFICATION, Action.FORWARD, Role.VILLAGE_ACCOUNTANT)
    assert result == State.RI_REVIEW


def test_ri_cannot_act_in_field_verification():
    with pytest.raises(InvalidTransition):
        next_state(State.FIELD_VERIFICATION, Action.FORWARD, Role.REVENUE_INSPECTOR)


def test_ri_review_pass_to_field_verification():
    result = next_state(State.RI_REVIEW, Action.RETURN_, Role.REVENUE_INSPECTOR)
    assert result == State.FIELD_VERIFICATION

def test_tahsildar_final_decision_approve():
    result = next_state(State.FINAL_DECISION, Action.APPROVE, Role.TAHSILDAR)
    assert result == State.APPROVED

def test_ri_cannot_approve():
    with pytest.raises(InvalidTransition):
        next_state(State.FINAL_DECISION, Action.APPROVE, Role.REVENUE_INSPECTOR)


def test_final_states_are_dead_ends():
    for state in (State.APPROVED, State.REJECTED):
        for action, role in product(Action, Role):
            with pytest.raises(InvalidTransition):
                next_state(state, action, role)

def test_states_for_role():
    assert states_for_role(Role.TAHSILDAR) == {State.FINAL_DECISION}
    assert State.FINAL_DECISION not in states_for_role(Role.VILLAGE_ACCOUNTANT)


def test_allowed_actions():
    assert allowed_actions(State.FINAL_DECISION, Role.TAHSILDAR) == {Action.APPROVE, Action.REJECT, Action.RETURN_}
    assert allowed_actions(State.FINAL_DECISION, Role.REVENUE_INSPECTOR) == set()
