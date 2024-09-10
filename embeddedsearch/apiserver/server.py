from fastapi import FastAPI
import uvicorn

from core.indexer import index_document
from core.searcher import search_documents
from core.pbutil import article_pb_unmarshal
import xxhash

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to Embedded Search Engine!"

@app.post("/index_one")
async def index_one(document: dict):
    index_document(xxhash.xxh64_hexdigest(document["links"]),document)
    return {"message": "Document added successfully"}


@app.get("/search")
async def search(q: str,page: int = 1):
    result=search_documents(q,offset=(page-1)*20,limit=20)
    resp={}
    if "data" in result.keys() :
        
        resp["records"]=[article_pb_unmarshal(r) for r in result["data"]]
        resp["total"]=result["total"]
        return resp
    return resp
    
def serve():
    uvicorn.run(app, host="0.0.0.0", port=8000)