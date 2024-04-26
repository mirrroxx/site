import sqlalchemy
from .db_session import SqlAlchemyBase


class Dishes(SqlAlchemyBase):
    __tablename__ = 'dishes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.time}, {self.price}, {self.photo}"