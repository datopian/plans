from contextlib import contextmanager
from typing import Tuple

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker, relationship

from .config import database_url

# ## SQL DB
assert database_url is not None, "No database defined, please set your DATABASE_URL environment variable"
sql_engine = create_engine(database_url)

Base = declarative_base()
sql_session = sessionmaker(bind=sql_engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = sql_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.expunge_all()


# ## DB Schema

class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    plan_name = Column(String(128))
    max_public_storage_mb = Column(Integer)
    max_private_storage_mb = Column(Integer)
    max_dataset_num = Column(Integer)

    def __str__(self):
        return self.plan_name


class UserPlan(Base):
    __tablename__ = 'user_plans'
    id = Column(Integer, primary_key=True)
    userid = Column(String(128), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    plan = relationship("Plan", foreign_keys=[plan_id])

# Create tables
Base.metadata.create_all(sql_engine)


def get_user(userid_) -> Tuple[UserPlan, Plan]:
    with session_scope() as session:
        user = session.query(UserPlan).filter_by(userid=userid_).first()
        yield user


def get_plan(plan_name) -> Plan:
    with session_scope() as session:
        yield session.query(Plan).filter_by(plan_name=plan_name).first()
