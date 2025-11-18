import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Transit, Accident, Roadwork

app = FastAPI(title="Traffic Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Traffic Intelligence API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# -------------------------
# Traffic data endpoints
# -------------------------

class CreateTransit(Transit):
    pass

class CreateAccident(Accident):
    pass

class CreateRoadwork(Roadwork):
    pass

@app.get("/api/transit", response_model=List[Transit])
def list_transit(limit: int = 50):
    try:
        docs = get_documents("transit", limit=limit)
        # sanitize _id and convert timestamps to strings
        for d in docs:
            d.pop("_id", None)
            if "created_at" in d:
                d["created_at"] = str(d["created_at"]) 
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"]) 
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transit")
def create_transit(payload: CreateTransit):
    try:
        _id = create_document("transit", payload)
        return {"ok": True, "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/accidents", response_model=List[Accident])
def list_accidents(limit: int = 50, status: Optional[str] = None):
    try:
        filter_dict = {"status": status} if status else None
        docs = get_documents("accident", filter_dict=filter_dict, limit=limit)
        for d in docs:
            d.pop("_id", None)
            if "created_at" in d:
                d["created_at"] = str(d["created_at"]) 
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"]) 
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/accidents")
def create_accident(payload: CreateAccident):
    try:
        _id = create_document("accident", payload)
        return {"ok": True, "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/roadworks", response_model=List[Roadwork])
def list_roadworks(limit: int = 50, status: Optional[str] = None):
    try:
        filter_dict = {"status": status} if status else None
        docs = get_documents("roadwork", filter_dict=filter_dict, limit=limit)
        for d in docs:
            d.pop("_id", None)
            if "created_at" in d:
                d["created_at"] = str(d["created_at"]) 
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"]) 
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/roadworks")
def create_roadwork(payload: CreateRoadwork):
    try:
        _id = create_document("roadwork", payload)
        return {"ok": True, "id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
