# Здесь все роутеры эндпоинтов подключаются к одному главному.
from fastapi import APIRouter

from app.api.endpoints.car import router as car_router
from app.api.endpoints.pipeline import router as pipeline_router
from app.api.endpoints.run_pipeline import router as run_pipeline_router
from app.api.endpoints.step import router as step_router

main_router = APIRouter()
main_router.include_router(car_router)
main_router.include_router(pipeline_router)
main_router.include_router(step_router)
main_router.include_router(run_pipeline_router)
