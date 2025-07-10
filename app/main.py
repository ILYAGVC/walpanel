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
from app.routers.pruchase_router.plan_post import router as purchase_post
from app.routers.pruchase_router.plan_get import router as purchase_get
from app.routers.pruchase_router.payment_post import router as payment_post
from app.routers.pruchase_router.payment_get import router as payment_get
from app.routers.mainadmin_router.backup_restore import router as backup_restore
from app.routers.pruchase_router.extopay_payment import router as extopay_payment
from app.middleware import RedirectUnauthorizedMiddleware



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data/receipts", StaticFiles(directory="data/receipts"), name="receipts")
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
app.include_router(purchase_post)
app.include_router(purchase_get)
app.include_router(payment_post)
app.include_router(payment_get)
app.include_router(backup_restore)
app.include_router(extopay_payment)



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
