from app.models.user import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def create(self, email, password_hash, role, status):
        user = User(email=email, password_hash=password_hash, role=role, status=status)
        self.session.add(user)
        return user

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()
