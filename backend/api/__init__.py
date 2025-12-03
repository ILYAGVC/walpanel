from .superadmin.routers import router as superadmin_routers
from .public.routers import router as public_routers

roter_list = [superadmin_routers, public_routers]
