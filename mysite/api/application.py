from mysite.database.models import Application, UserProfile, RoleChoices, Course, CourseStatus
from mysite.database.schema import ApplicationInputSchema, ApplicationOutSchema
from mysite.database.db import SessionLocal
from mysite.api.auth import get_current_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List

application_router = APIRouter(prefix='/application', tags=['Application'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@application_router.post('/', response_model=ApplicationOutSchema)
async def create_application(application:ApplicationInputSchema, db:Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    if current_user.role != RoleChoices.student:
        raise HTTPException(status_code=403, detail='Создать заявку может только студент')
    course_db = db.query(Course).filter(Course.id==application.course_id).first()
    if not course_db:
        raise HTTPException(detail='Мындай курс жок', status_code=404)
    if current_user.status == True and course_db.status != CourseStatus.free:
        raise HTTPException(status_code=403, detail='Неактивный студент может создать заявку только на бесплатный курс')
    application_data = application.model_dump()
    application_data['student_id'] = current_user.id
    application_db = Application(**application_data)
    db.add(application_db)
    db.commit()
    db.refresh(application_db)
    return application_db


@application_router.get('/', response_model=List[ApplicationOutSchema])
async def list_application(db: Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    if current_user.role != RoleChoices.manager:
        raise HTTPException(status_code=403, detail='Список заявок может смотреть только менеджер')
    return db.query(Application).all()


@application_router.get('/{application_id}/', response_model=ApplicationOutSchema)
async def detail_application(application_id: int, db:Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    if current_user.role != RoleChoices.manager:
        raise HTTPException(status_code=403, detail='Заявку может смотреть только менеджер')
    application = db.query(Application).filter(Application.id==application_id).first()
    if not application:
        raise HTTPException(detail='Мындай заявка жок', status_code=404)
    return application


@application_router.put('/{application_id}/', response_model=dict)
async def update_application(application_id: int, application: ApplicationInputSchema, db: Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    if current_user.role != RoleChoices.manager:
        raise HTTPException(status_code=403, detail='Изменить заявку может только менеджер')
    application_db = db.query(Application).filter(Application.id==application_id).first()
    if not application_db:
        raise HTTPException(detail='Мындай заявка жок', status_code=404)
    for application_key, application_value in application.model_dump().items():
        setattr(application_db, application_key, application_value)
    db.commit()
    db.refresh(application_db)
    return {'message': 'Заявка озгорулду'}


@application_router.delete('/{application_id}/', response_model=dict)
async def delete_application(application_id: int, db: Session = Depends(get_db), current_user:UserProfile = Depends(get_current_user)):
    if current_user.role != RoleChoices.manager:
        raise HTTPException(status_code=403, detail='Удалить заявку может только менеджер')
    application_db = db.query(Application).filter(Application.id==application_id).first()
    if not application_db:
        raise HTTPException(detail='Мындай заявка жок', status_code=404)
    db.delete(application_db)
    db.commit()
    return {'message': 'Заявка удалить болду'}