from app.models.activity_log import ActivityLog


def log_activity(
    db,
    user_id,
    business_id,
    action
):

    log = ActivityLog(
        user_id=user_id,
        business_id=business_id,
        action=action
    )

    db.add(log)
    db.commit()