from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict
from .models import RoleChoices, LevelChoices, CourseStatus, StudyStatus, EnrollmentStatus, ApplicationStatus
from datetime import date, datetime

class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    phone_number: Optional[str] = None
    role: RoleChoices = RoleChoices.student
    status: bool = True


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    age: Optional[int] = None
    phone_number: Optional[str] = None
    role: RoleChoices
    status: bool
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}


class CategoryInputSchema(BaseModel):
    category_name: str

class CategoryOutSchema(BaseModel):
    id: int
    category_name: str

class CourseInputSchema(BaseModel):
    title: str
    description: str
    level: list[LevelChoices]
    price: int
    duration_weeks: int
    is_active: bool
    status: CourseStatus
    category_id: int

class CourseOutSchema(BaseModel):
    id: int
    title: str
    description: str
    level: list[LevelChoices]
    price: int
    duration_weeks: int
    is_active: bool
    status: CourseStatus
    created_at: datetime
    updated_at: datetime
    category_id: int

class StudyGroupInputSchema(BaseModel):
    name: str
    teacher_id: int
    starts_on: date
    ends_on: date
    study_status: StudyStatus
    course_id: int

class StudyGroupOutSchema(BaseModel):
    id: int
    name: str
    teacher_id: int
    starts_on: date
    ends_on: date
    study_status: StudyStatus
    created_at: datetime
    updated_at: datetime
    course_id: int

class ApplicationInputSchema(BaseModel):
    comment: str | None = None
    course_id: int

class ApplicationOutSchema(BaseModel):
    id: int
    student_id: int
    manager_id: int | None
    comment: str | None
    application_status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    course_id: int

class EnrollmentInputSchema(BaseModel):
    student_id: int
    enrollment_status: EnrollmentStatus
    group_id: int

class EnrollmentOutSchema(BaseModel):
    id: int
    student_id: int
    enrollment_status: EnrollmentStatus
    created_at: datetime
    updated_at: datetime
    group_id: int

class CurrentUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str