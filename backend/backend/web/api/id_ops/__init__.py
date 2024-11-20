from fastapi import APIRouter

from backend.web.api.id_ops import views

router = APIRouter(prefix="/id", tags=["ID Operations"])
router.include_router(views.router)