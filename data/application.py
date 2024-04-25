import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .db_session import SqlAlchemyBase


class application(SqlAlchemyBase, UserMixin):
    __tablename__ = 'application'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    grade = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    balance = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    role = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
