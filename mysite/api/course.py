from mysite.database.models import Course, UserProfile, RoleChoices
from mysite.database.schema import CourseInputSchema, CourseOutSchema
from mysite.database.db import SessionLocal
from mysite.api.auth import get_current_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List

course_router = APIRouter(prefix='/course', tags=['Course'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@course_router.post('/', response_model=CourseOutSchema)
async def create_course(course:CourseInputSchema, db:Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    if current_user.role != RoleChoices.teacher:
        raise HTTPException(status_code=403, detail='Создать курс может только учитель')
    course_db = Course(**course.model_dump())
    db.add(course_db)
    db.commit()
    db.refresh(course_db)
    return course_db


@course_router.get('/', response_model=List[CourseOutSchema])
async def list_course(db: Session = Depends(get_db)):
    return db.query(Course).all()


@course_router.get('/{course_id}/', response_model=CourseOutSchema)
async def detail_course(course_id: int, db:Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id==course_id).first()
    if not course:
        raise HTTPException(detail='Мындай курс жок', status_code=404)
    return course


@course_router.put('/{course_id}/', response_model=dict)
async def update_course(course_id: int, course: CourseInputSchema, db: Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    course_db = db.query(Course).filter(Course.id==course_id).first()
    if not course_db:
        raise HTTPException(detail='Мындай курс жок', status_code=404)
    if current_user.role != RoleChoices.teacher:
        raise HTTPException(status_code=403, detail='Изменить курс может только учитель')
    for course_key, course_value in course.model_dump().items():
        setattr(course_db, course_key, course_value)
    db.commit()
    db.refresh(course_db)
    return {'message': 'Курс озгорулду'}


@course_router.delete('/{course_id}/', response_model=dict)
async def delete_course(course_id: int, db: Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    course_db = db.query(Course).filter(Course.id==course_id).first()
    if not course_db:
        raise HTTPException(detail='Мындай курс жок', status_code=404)
    if current_user.role != RoleChoices.teacher:
        raise HTTPException(status_code=403, detail='Удалить курс может только учитель')
    db.delete(course_db)
    db.commit()
    return {'message': 'Курс удалить болду'}