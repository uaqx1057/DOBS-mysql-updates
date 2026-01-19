from flask_mail import Message
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
