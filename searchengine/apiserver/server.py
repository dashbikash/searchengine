from fastapi import FastAPI,APIRouter
import uvicorn

from core.news_engine import NewsIndexer,NewsSearcher

app = FastAPI()

api_router=APIRouter(prefix= "/api")


@api_router.post("/index")
async def index_one(data: dict):
    if  len(data["documents"])>1000: 
        return {"message": "Document count exceeds limit"}
    try:
        indexer=NewsIndexer()
        indexer.new_batch()
        for doc in data["documents"]: indexer.index(doc)
        indexer.save_batch()
    except Exception as e:
        indexer.cancel_batch()
    finally:
        indexer.finish()
        return {"message": "Document added successfully"}


@api_router.get("/search")
async def search(q: str,page: int = 1):
    searcher =NewsSearcher()
    result=searcher.search(q,offset=(page-1)*20,limit=20)
    searcher.finish()
    return result

@app.get("/")
async def root():
    return "This is a Search Engine Project!"

app.include_router(api_router)
    
def serve():
    uvicorn.run(app, port=8619)