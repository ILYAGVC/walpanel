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

all_routers = [
    login,
    main_admin_dash,
    admin_dash,
    admin_post,
    panel_post,
    panel_get,
    mainadmin_post,
    mainadmin_get,
    news_post,
    news_get,
    purchase_post,
    purchase_get,
    payment_post,
    payment_get,
    backup_restore,
    extopay_payment
]