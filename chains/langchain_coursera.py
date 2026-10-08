from pathlib import Path
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore

BASE_DIR = Path(__file__).resolve().parent
loaders = TextLoader(str(BASE_DIR / 'base_knowledge.txt'), encoding='utf-8')
document = loaders.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=40
)

chunks = text_splitter.split_documents(document)

embeddings = OllamaEmbeddings(
    model='nomic-embed-text'
)

vectors_store = InMemoryVectorStore.from_documents(chunks, embeddings)

prompt = ChatPromptTemplate(
    [
        (
            'system',
            "Ты онлайн менеджер сайта Coursera. "
            "При ответе ты должен сначала посмотреть Базу Знаний: "
            "База знаний: {base_knowledge}. "
            "Должен отвечать на вопросы коротко и вежливо. "
            "Каждый курс перечисляй только один раз. "
            "Не повторяй один и тот же курс. "
            "Не придумывай информации которые нет в базе знаний. "
            "Если не нашел ответ в базе знаний, напиши что не знаешь."
        ),
        (
            'human',
            '{content}'
        )
    ]
)

model = ChatOllama(
    model='llama3.2:latest',
    temperature=0
)

chain = prompt | model | StrOutputParser()


def search_answer(question: str):
    new_document = vectors_store.similarity_search(question, k=1)
    final_answer = chain.invoke({
        'content': question,
        'base_knowledge': new_document
    })
    final_answer = final_answer.replace('\n', ' ')
    final_answer = final_answer.replace('*', '')
    final_answer = ' '.join(final_answer.split())

    return final_answer