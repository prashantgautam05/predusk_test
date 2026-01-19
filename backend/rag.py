from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI
from qdrant_client import QdrantClient
import cohere

client = OpenAI()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def answer_query(query):
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    results = qdrant.search(
        collection_name=os.getenv("COLLECTION_NAME"),
        query_vector=emb,
        limit=8
    )

    docs = [r.payload["text"] for r in results]

    rerank = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=docs,
        top_n=4
    )

    context = ""
    citations = []
    for i, r in enumerate(rerank.results):
        context += f"[{i+1}] {docs[r.index]}\n"
        citations.append(docs[r.index][:80])

    if not context.strip():
        return "No relevant information found.", []

    prompt = f"""
Answer the question using ONLY the context.
Add inline citations like [1], [2].

Context:
{context}

Question: {query}
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content, citations

