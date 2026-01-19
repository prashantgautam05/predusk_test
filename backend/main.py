from fastapi import FastAPI
from pydantic import BaseModel
from ingest import ingest
from rag import answer_query

app = FastAPI()

class Query(BaseModel):
    query: str
    text: str | None = None

@app.post("/query")
def query_rag(q: Query):
    if q.text:
        ingest(q.text)

    answer, sources = answer_query(q.query)
    return {
        "answer": answer,
        "sources": sources
    }

