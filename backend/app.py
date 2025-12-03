from fastapi import FastAPI

from backend.auth import auth_router
from backend.api import roter_list


app = FastAPI(
    title="WalPanel",
)

for router in roter_list:
    app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/api")
