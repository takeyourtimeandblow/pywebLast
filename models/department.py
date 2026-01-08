# models/department.py
import sqlalchemy as sa

from db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = "departments"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
    chief = sa.Column(sa.Integer)
    members = sa.Column(sa.String)
    email = sa.Column(sa.String)
