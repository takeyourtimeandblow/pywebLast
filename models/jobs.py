# models/jobs.py
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db_session import SqlAlchemyBase

job_category = sa.Table(
    "job_category",
    SqlAlchemyBase.metadata,
    sa.Column("job_id", sa.Integer, sa.ForeignKey("jobs.id")),
    sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")),
)


class Jobs(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    job = sa.Column(sa.String)
    work_size = sa.Column(sa.Integer)
    collaborators = sa.Column(sa.String)
    start_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    end_date = sa.Column(sa.DateTime)
    is_finished = sa.Column(sa.Boolean, default=False)

    leader = relationship("User", back_populates="jobs")

    categories = relationship("Category", secondary=job_category, backref="jobs")

    def __repr__(self):
        return f"<Job> {self.job}"
