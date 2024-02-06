from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import check_obj_exists
from app.core.db import get_async_session
from app.crud.car import car_crud
from app.models.car import Car
from app.schemas.car import CarSchema

router = APIRouter(prefix='/cars', tags=['Cars'])


@router.get('/', response_model=list[CarSchema],
            response_model_exclude_none=True)
async def get_all_cars(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить все машины из базы."""
    return await car_crud.get_multi(session=session)


@router.get('/{car_id}', response_model=CarSchema,
            response_model_exclude_none=True)
async def get_car(car_id: int,
                  session: AsyncSession = Depends(get_async_session)):
    """Получить машину."""
    car = await check_obj_exists(Car, car_id, session)
    return car


@router.delete('/{car_id}',
               response_model_exclude_none=True)
async def remove_car(car_id: int,
                     session: AsyncSession = Depends(get_async_session)):
    """Удалить машину."""
    car = await check_obj_exists(Car, car_id, session)
    car = await car_crud.remove(car, session)
    return car
