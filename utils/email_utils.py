from flask import current_app
from flask_mail import Message
from threading import Thread
from extensions import mail

def send_password_change_email(user, new_password):
    try:
        msg = Message(
            subject="Your Password Has Been Changed",
            recipients=[user.email],
            sender="noreply@yourdomain.com"
        )
        msg.body = f"""
Hello {user.username},

Your password has been successfully changed.

Username: {user.username}
New Password: {new_password}

If you did not make this change, please contact support immediately.

Best regards,
DOBS System Team
"""
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending password change email: {e}")
        return False


def _send_async_email(app, msg, logger=None):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as exc:
            if logger:
                logger.exception("Email send failed")
            else:
                print(f"Email send failed: {exc}")


def safe_send_email(msg: Message, logger=None, background=True):
    """Send email with optional background thread and logging."""
    app = current_app._get_current_object()
    if background:
        Thread(target=_send_async_email, args=(app, msg, logger), daemon=True).start()
        return True

    try:
        mail.send(msg)
        return True
    except Exception as exc:
        if logger:
            logger.exception("Email send failed")
        else:
            print(f"Email send failed: {exc}")
        return False
