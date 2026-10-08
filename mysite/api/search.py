from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from chains.langchain_coursera import search_answer

search_router = APIRouter(prefix='/search', tags=['Search'])

class QuestionSchema(BaseModel):
    question: str

@search_router.post('/questions/')
async def answer(data: QuestionSchema):
    question = data.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail='Маалымат берилген жок')
    final_answer = search_answer(question)
    return {'answer': final_answer}