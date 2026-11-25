from sqlmodel import Session
from models import Application, History
from workflow import next_state


#  a service layer encapsulates business logic and coordinates operation btw api layer, domain logic
# and persistence layer.



# session we can think of it as your application's working conv with db it lets you retrieve records, ins, update, delete, commit and roll back trans
def perform_action(session: Session, application_id: int, action, role, actor_name: str, reason: str = ""):
    application = session.get(Application, application_id)
    if application is None:
        raise ValueError("Application not found")

    old_status = application.status
    new_status = next_state(old_status, action, role)

    # modifying python obj associated with sqlalchmey session (the ORM tracks this change) called dirty tracking
    application.status = new_status

    # sqlmodel models accpet keyword arguments only
    history = History(
        application_id=application_id,
        from_state=old_status.value,
        to_state=new_status.value,
        action=action.value,
        role=role.value,
        actor_name=actor_name,
        reason=reason
    )

    session.add(history)
    session.commit()
    session.refresh(application)
    return application

