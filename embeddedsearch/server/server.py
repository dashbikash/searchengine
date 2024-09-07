from fastapi import FastAPI
import uvicorn

from core.indexer import index_document
from core.searcher import search_documents

app = FastAPI()

@app.post("/index_one")
async def index_one(document: dict):
    index_document(document)
    return {"message": "Document added successfully"}


@app.get("/search")
async def search(query: str,page: int = 1):
    return search_documents(query,offset=(page-1)*10,pagesize=10)
    
def serve():
    uvicorn.run(app, host="0.0.0.0", port=8000)