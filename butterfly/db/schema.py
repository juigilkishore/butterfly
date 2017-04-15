from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, BLOB
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, UniqueConstraint

from butterfly.utils.utils import get_uuid, get_utc_time

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint('email', 'phone'),)
    id = Column(String(36), primary_key=True, default=get_uuid)
    name = Column(String(24), nullable=False)
    age = Column(Integer, nullable=False)
    # TODO(juigil): Add gender constraint
    gender = Column(String(10), nullable=False)
    email = Column(String(24), unique=True, nullable=False)
    phone = Column(String(16), nullable=False)
    joined_at = Column(DateTime, nullable=False, default=get_utc_time)
    last_updated_at = Column(DateTime, nullable=False, default=get_utc_time)


class Lesson(Base):
    __tablename__ = "lesson"
    id = Column(String(36), primary_key=True, default=get_uuid)
    name = Column(String(24), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    week = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False, unique=True, autoincrement=True)
    is_active = Column(Boolean, nullable=False, default=True)


class Goal(Base):
    __tablename__ = "goal"
    id = Column(String(36), primary_key=True, default=get_uuid)
    name = Column(String(24), nullable=False)
    description = Column(Text, nullable=False)
    reason = Column(String(36), ForeignKey(Lesson.__tablename__ + ".id"))
    week = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    effects = Column(BLOB, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)


class ActivityLesson(Base):
    __tablename__ = "activity_lesson"
    __table_args__ = (PrimaryKeyConstraint('user_id', 'lesson_id'),)
    user_id = Column(String(36), ForeignKey(User.__tablename__ + ".id"), nullable=False)
    lesson_id = Column(String(36), ForeignKey(Lesson.__tablename__ + ".id"), nullable=False)
    opened_at = Column(DateTime, nullable=False, default=get_utc_time)
    completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime, nullable=True)


class ActivityGoal(Base):
    __tablename__ = "activity_goal"
    __table_args__ = (PrimaryKeyConstraint('user_id', 'goal_id'),)
    user_id = Column(String(36), ForeignKey(User.__tablename__ + ".id"), nullable=False)
    goal_id = Column(String(36), ForeignKey(Goal.__tablename__ + ".id"), nullable=False)
    frequency = Column(Integer, nullable=False, default=1)
    last_updated_at = Column(DateTime, nullable=False, default=get_utc_time)
    completed_on = Column(BLOB, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
