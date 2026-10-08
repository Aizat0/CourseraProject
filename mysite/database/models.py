from .db import Base
from sqlalchemy import String, Integer, ForeignKey, Date, DateTime, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import date, datetime
from enum import Enum


class RoleChoices(str, Enum):
    student = 'student'
    teacher = 'teacher'
    manager = 'manager'
    admin = 'admin'


class UserProfile(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    age: Mapped[int] = mapped_column(Integer)
    phone_number: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleChoices] = mapped_column(SQLEnum(RoleChoices), default=RoleChoices.student)
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user',
                                                            cascade='all, delete-orphan')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(100), unique=True)
    category_course: Mapped[List["Course"]] = relationship('Course', back_populates='category', cascade='all, delete-orphan')


class LevelChoices(str, Enum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'


class CourseStatus(str, Enum):
    free = 'free'
    plus = 'plus'


class Course(Base):
    __tablename__ = 'course'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(200))
    level: Mapped[list[LevelChoices]] = mapped_column(JSON, default=list)
    price: Mapped[int] = mapped_column(Integer)
    duration_weeks: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean)
    status: Mapped[CourseStatus] = mapped_column(SQLEnum(CourseStatus), default=CourseStatus.free)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(Category, back_populates='category_course')
    course_study: Mapped[List["StudyGroup"]] = relationship('StudyGroup', back_populates='course', cascade='all, delete-orphan')
    course_application: Mapped[List["Application"]] = relationship('Application', back_populates='course', cascade='all, delete-orphan')


class StudyStatus(str, Enum):
    recruiting = 'recruiting'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class StudyGroup(Base):
    __tablename__ = 'group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150))
    teacher_id: Mapped[int] = mapped_column(Integer)
    starts_on: Mapped[date] = mapped_column(Date, default=date.today)
    ends_on: Mapped[date] = mapped_column(Date, default=date.today)
    study_status: Mapped[StudyStatus] = mapped_column(SQLEnum(StudyStatus), default=StudyStatus.recruiting)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='course_study')
    group_enrollment: Mapped[List["Enrollment"]] = relationship('Enrollment', back_populates='enrollment_group', cascade='all, delete-orphan')


class ApplicationStatus(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    accepted = 'accepted'
    rejected = 'rejected'
    cancelled = 'cancelled'


class Application(Base):
    __tablename__ = 'application'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer)
    manager_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
    application_status: Mapped[ApplicationStatus] = mapped_column(SQLEnum(ApplicationStatus), default=ApplicationStatus.new)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship(Course, back_populates='course_application')


class EnrollmentStatus(str, Enum):
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'


class Enrollment(Base):
    __tablename__ = 'enrollment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer)
    enrollment_status: Mapped[EnrollmentStatus] = mapped_column(SQLEnum(EnrollmentStatus), default=EnrollmentStatus.active)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_id: Mapped[int] = mapped_column(ForeignKey('group.id'))
    enrollment_group: Mapped[StudyGroup] = relationship(StudyGroup, back_populates='group_enrollment')