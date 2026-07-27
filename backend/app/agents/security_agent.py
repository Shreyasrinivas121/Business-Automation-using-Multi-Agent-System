from app.models.security_alert import SecurityAlert


def create_alert(
    db,
    user_id,
    business_id,
    alert_type,
    message,
    severity,
    voice_message=None
):

    alert = SecurityAlert(
        user_id=user_id,
        business_id=business_id,
        alert_type=alert_type,
        message=message,
        severity=severity,
        status="Active",
        voice_message=voice_message
    )

    db.add(alert)

    db.commit()