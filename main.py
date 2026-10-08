from fastapi import FastAPI
import uvicorn
from mysite.database.db import Base, engine
from mysite.api import auth, user, course, category, application, enrollment, group, search

Base.metadata.create_all(bind=engine)
coursera_app = FastAPI(title='Coursera Project')
coursera_app.include_router(auth.auth_router)
coursera_app.include_router(user.user_router)
coursera_app.include_router(category.category_router)
coursera_app.include_router(course.course_router)
coursera_app.include_router(application.application_router)
coursera_app.include_router(enrollment.enrollment_router)
coursera_app.include_router(group.study_group_router)
coursera_app.include_router(search.search_router)



if __name__ == '__main__':
    uvicorn.run(coursera_app, host='127.0.0.1', port=8004)