from app import db
from app.models import User


def is_admin(user_id):
    if user_id is None:
        return False

    user = db.session.query(User).filter_by(id=user_id).first()

    return user.flags & User.FlagsBit.ADMIN_BIT > 0
