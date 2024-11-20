from fastapi.routing import APIRouter

from backend.web.api import monitoring, id_ops

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(id_ops.router)
