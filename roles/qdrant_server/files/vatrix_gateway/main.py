# vatrix_gateway/main.py

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from qdrant_client.http.exceptions import ResponseHandlingException
import os, logging
import time


app = FastAPI(title="Vatrix Gateway API", version="0.1.0")
logging.basicConfig(level=logging.INFO)

COLLECTION_NAME = "vatrix_gateway_logs"
qdrant = None

# ------------------------------
# Qdrant Setup
# ------------------------------
@app.on_event("startup")
async def startup_event():
    global qdrant
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6334))

    qdrant = QdrantClient(
        host=QDRANT_HOST,
        grpc_port=QDRANT_PORT,
        prefer_grpc=True,
        port=None,
        https=False,
        timeout=30.0
    )

    for attempt in range(10):
        try:
            qdrant.get_collection(collection_name=COLLECTION_NAME)
            logging.info(f"✅ Connected to Qdrant via gRPC at {QDRANT_HOST}:{QDRANT_PORT}")
            break
        except Exception:
            try:
                qdrant.recreate_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                logging.info("✅ Created Qdrant collection")
                break
            except ResponseHandlingException as e:
                logging.warning(f"Waiting for Qdrant... attempt {attempt + 1}/10")
                time.sleep(3)
    else:
        logging.error("❌ Could not connect to Qdrant after retries.")

@app.get("/health")
async def healthcheck():
    try:
        qdrant.get_collection(collection_name="vatrix_gateway_logs")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# ------------------------------
# Pydantic Models
# ------------------------------
class LogEntry(BaseModel):
    id: str = Field(..., example="log-001")
    vector: List[float]
    payload: Dict[str, str]
    timestamp: datetime

class IngestRequest(BaseModel):
    project: str
    entries: List[LogEntry]

class SearchQuery(BaseModel):
    query_vector: List[float]
    top_k: int = 3

# ------------------------------
# API Router
# ------------------------------
router = APIRouter(prefix="/api/v1")

@router.post("/ingest")
async def ingest_logs(request: IngestRequest):
    try:
        logging.info("📥 Received ingest request")
        points = [
            PointStruct(id=entry.id, vector=entry.vector, payload=entry.payload)
            for entry in request.entries
        ]
        logging.info(f"🧠 Inserting {len(points)} points into collection {COLLECTION_NAME}")
        result = qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
        logging.info(f"✅ Qdrant upsert result: {result}")
        return {"status": "ok", "ingested": len(points), "project": request.project}
    except Exception as e:
        logging.exception("❌ Error during ingestion")
        return {"status": "error", "detail": str(e)}

@router.post("/search")
async def search_logs(query: SearchQuery):
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query.query_vector,
        limit=query.top_k
    )
    return [
        {"log_text": hit.payload.get("log_text"), "score": hit.score}
        for hit in results
    ]

app.include_router(router)

# ------------------------------
# Run Uvicorn
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)