import datetime

import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    surname = sa.Column(sa.String)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    position = sa.Column(sa.String)
    speciality = sa.Column(sa.String)
    address = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    city_from = sa.Column(sa.String)
    hashed_password = sa.Column(sa.String)
    modified_date = sa.Column(sa.DateTime, default=datetime.datetime.now)

    jobs = relationship("Jobs", back_populates="leader")

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"
