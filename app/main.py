from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
import os

from app.routers import all_routers
from app.middleware import RedirectUnauthorizedMiddleware
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


DOCS = "/docs" if os.getenv("DOCS").lower() == "true" else None

app = FastAPI(docs_url=DOCS)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data/receipts", StaticFiles(directory="data/receipts"), name="receipts")
app.add_middleware(RedirectUnauthorizedMiddleware)


for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
