import sqlalchemy as sa

from db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = "categories"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)

    def __repr__(self):
        return f"<Category> {self.title}"
