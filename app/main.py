from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn

from app.auth.auth_controller import router as login
from app.routers.mainadmin_router.main_admin_dash import router as main_admin_dash
from app.routers.admin_router.admin_dash import router as admin_dash
from app.routers.admin_router.admin_post import router as admin_post
from app.routers.mainadmin_router.panel_post import router as panel_post
from app.routers.mainadmin_router.panel_get import router as panel_get
from app.routers.mainadmin_router.admin_post import router as mainadmin_post
from app.routers.mainadmin_router.admin_get import router as mainadmin_get
from app.routers.mainadmin_router.news_post import router as news_post
from app.routers.mainadmin_router.news_get import router as news_get
from app.middleware import RedirectUnauthorizedMiddleware

# from app.routers.extopay_payment import router as payment_router


app = FastAPI(docs_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(RedirectUnauthorizedMiddleware)

app.include_router(login)
app.include_router(main_admin_dash)
app.include_router(mainadmin_get)
app.include_router(mainadmin_post)
app.include_router(admin_dash)
app.include_router(admin_post)
app.include_router(panel_get)
app.include_router(panel_post)
app.include_router(news_post)
app.include_router(news_get)
# app.include_router(payment_router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
