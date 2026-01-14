
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.rag import answer


app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class Query(BaseModel):
    question: str

@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.post("/chat")
def chat(q: Query):
    return {"answer": answer(q.question)}

### A warm-up event to load the model (sentence-transformers etc.) on startup and avoid long answering delay for the first question. ###
@app.on_event("startup")
def warmup():
    answer("Hello")