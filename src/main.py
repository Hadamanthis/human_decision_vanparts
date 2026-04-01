import dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from graph import build_graph
from api.route import router

dotenv.load_dotenv()

app = FastAPI()
app.state.graph = build_graph()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)