from .routes import Routes
from app.services.auth import router as auth_router
from app.internal import router_handlers

__routes__ = Routes((auth_router, router_handlers))
