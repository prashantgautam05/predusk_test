# Mini RAG – AI Engineer Assessment

## Architecture
FastAPI backend + Qdrant Cloud vector DB + OpenAI embeddings + Cohere reranker.

## Chunking
- Size: 1000 tokens
- Overlap: 10%

## Retrieval
- Top-8 vector search
- Cohere rerank (top-4)

## LLM
- GPT-4o-mini
- Inline citations [1], [2]

## Deployment
- Backend: Render
- Frontend: Vercel

## Limitations
- No PDF parsing
- Simple UI
- Approximate token cost
