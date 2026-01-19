import os, uuid, tiktoken
from qdrant_client import QdrantClient
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION = os.getenv("COLLECTION_NAME")
EMBED_MODEL = "text-embedding-3-small"

def chunk_text(text, size=1000, overlap=100):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []

    for i in range(0, len(tokens), size - overlap):
        chunk = tokens[i:i+size]
        chunks.append(enc.decode(chunk))
    return chunks

def ingest(text, source="user-upload"):
    chunks = chunk_text(text)

    vectors = []
    for i, chunk in enumerate(chunks):
        emb = client.embeddings.create(
            model=EMBED_MODEL,
            input=chunk
        ).data[0].embedding

        vectors.append({
            "id": str(uuid.uuid4()),
            "vector": emb,
            "payload": {
                "text": chunk,
                "source": source,
                "position": i
            }
        })

    qdrant.upsert(
        collection_name=COLLECTION,
        points=vectors
    )
