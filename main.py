from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import create_document, get_documents, db
from schemas import Lead

app = FastAPI(title="BPO Company API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "BPO API running"}


@app.get("/test")
def test_db():
    try:
        # simple ping by listing collections
        collections = db.list_collection_names() if db else []
        return {"ok": True, "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/leads")
def create_lead(lead: Lead):
    try:
        inserted_id = create_document("lead", lead)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads")
def list_leads(limit: Optional[int] = 50):
    try:
        docs = get_documents("lead", limit=limit)
        # Convert ObjectId to str
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])  # simple serialization
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"])  # simple serialization
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
