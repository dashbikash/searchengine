from fastapi import FastAPI,APIRouter
import uvicorn

from core.news_engine import NewsIndexer,NewsSearcher
import logging


app = FastAPI()

api_router=APIRouter(prefix= "/api")

@app.get("/")
async def root():
    return "This is a Search Engine Project!"

app.include_router(api_router)
    
def serve():
    uvicorn.run(app, host="0.0.0.0", port=8000)