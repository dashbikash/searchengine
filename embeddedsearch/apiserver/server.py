from fastapi import FastAPI
import uvicorn

from core.article_engine import ArticleIndexer,ArticleSearcher

app = FastAPI()

@app.get("/")
async def root():
    return "Welcome to Embedded Search Engine!"

@app.post("/index_one")
async def index_one(document: dict):
    indexer=ArticleIndexer()
    indexer.index(document)
    indexer.dispose()
    return {"message": "Document added successfully"}


@app.get("/search")
async def search(q: str,page: int = 1):
    searcher =ArticleSearcher()
    result=searcher.search(q,offset=(page-1)*20,limit=20)
    searcher.dispose()
    
    return result
    
def serve():
    uvicorn.run(app, host="0.0.0.0", port=8000)