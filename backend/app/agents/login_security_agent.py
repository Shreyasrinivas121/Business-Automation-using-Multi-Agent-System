from app.models.login_attempt import LoginAttempt
from app.agents.security_agent import create_alert


def record_failed_login(
    db,
    email,
    user=None
):

    attempt = db.query(
        LoginAttempt
    ).filter(
        LoginAttempt.email == email
    ).first()

    if not attempt:

        attempt = LoginAttempt(
            email=email,
            attempt_count=1
        )

        db.add(attempt)

        db.commit()

        return

    attempt.attempt_count += 1

    db.commit()

    if attempt.attempt_count >= 3:

        if email == "admin@gmail.com":

            create_alert(
                db=db,
                user_id=None,
                alert_type="Admin Login Attack",
                message=f"Someone is trying to access admin account ({email})",
                severity="High",
                voice_message=(
                    "Attention Administrator. "
                    "Multiple failed login attempts "
                    "have been detected on the administrator account."
                )
            )

        else:

            create_alert(
                db=db,
                user_id=user.id if user else None,
                alert_type="User Login Attack",
                message=f"{email} exceeded allowed login failures",
                severity="High",
                voice_message=(
                    f"Attention Administrator. "
                    f"User {email} has crossed "
                    f"the allowed login failure threshold."
                )
            )
            
def reset_login_attempts(
    db,
    email
):

    attempt = db.query(
        LoginAttempt
    ).filter(
        LoginAttempt.email == email
    ).first()

    if attempt:

        attempt.attempt_count = 0

        db.commit()            