# Clean FastAPI app with no embedding logic, ready to receive vector input from Vatrix
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams
import uvicorn

app = FastAPI()

# Connect to Qdrant
qdrant = QdrantClient("localhost", port=6333)
collection_name = "your_logs"

# Ensure collection exists
try:
    qdrant.get_collection(collection_name=collection_name)
except Exception:
    qdrant.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

class LogVector(BaseModel):
    log_id: int
    vector: List[float]
    payload: dict

class SearchQuery(BaseModel):
    query_vector: List[float]
    top_k: int = 3

@app.post("/add_log/")
async def add_log(entry: LogVector):
    qdrant.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=entry.log_id, vector=entry.vector, payload=entry.payload)]
    )
    return {"message": "Log stored", "log_id": entry.log_id}

@app.post("/search_logs/")
async def search_logs(query: SearchQuery):
    results = qdrant.search(
        collection_name=collection_name,
        query_vector=query.query_vector,
        limit=query.top_k
    )
    return [
        {"log_text": hit.payload["log_text"], "score": hit.score}
        for hit in results
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)