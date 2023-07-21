from .routes import Routes
from app.services.auth import router as auth_router
from app.internal import router_handlers
from app.internal import router_pages

__routes__ = Routes((auth_router, router_handlers, router_pages))
