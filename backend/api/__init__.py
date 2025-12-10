from .superadmin.routers import router as superadmin_routers
from .admin.routers import router as admin_routers
from .public.routers import router as public_routers

roter_list = [superadmin_routers, admin_routers, public_routers]
