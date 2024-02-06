from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.pipeline import pipeline_crud
from app.crud.step import step_crud
from app.models.pipeline import Pipeline
from app.models.step import Step


async def create_first_pipeline(session: AsyncSession):
    """Creates first pipeline and steps for it."""
    car_detection_pipeline = await pipeline_crud.get_by_attribute(
        'name',
        'Car_detection_pipeline',
        session)
    image_processing_step = await step_crud.get_by_attribute(
        'name',
        'Image_processing_step',
        session)
    ml_model_step = await step_crud.get_by_attribute(
        'name',
        'ML_model_step',
        session)
    db_save_step = await step_crud.get_by_attribute(
        'name',
        'DB_save_step',
        session)

    if car_detection_pipeline is None:
        pipeline_data = {
            'name': 'Car_detection_pipeline',
            'description': 'Detects car on image'
        }
        car_detection_pipeline = Pipeline(**pipeline_data)
        session.add(car_detection_pipeline)
        await session.commit()
        await session.refresh(car_detection_pipeline)

    if image_processing_step is None:
        step_data = {
            'name': 'Image_processing_step',
            'description': 'Processing image',
            'func': 'process_image'
        }
        image_processing_step = Step(**step_data)
        session.add(image_processing_step)
        await session.commit()
        await session.refresh(image_processing_step)

    if ml_model_step is None:
        step_data = {
            'name': 'ML_model_step',
            'description': 'Processing image trough ML model',
            'func': 'ml_process_image'
        }
        ml_model_step = Step(**step_data)
        session.add(ml_model_step)
        await session.commit()
        await session.refresh(ml_model_step)

    if db_save_step is None:
        step_data = {
            'name': 'DB_save_step',
            'description': 'Saving image to DB',
            'func': 'save_result'
        }
        db_save_step = Step(**step_data)
        session.add(db_save_step)
        await session.commit()
        await session.refresh(db_save_step)

    steps = [image_processing_step,
             ml_model_step,
             db_save_step]

    for obj in steps:
        step_data = {'step': obj}
        await pipeline_crud.add_step(car_detection_pipeline,
                                     step_data,
                                     session)


async def check_obj_exists(model: object,
                           obj_id: int,
                           session: AsyncSession) -> object:
    crud = CRUDBase(model)
    obj = await crud.get_by_attribute('id', obj_id, session)
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Объект не найден!"
        )
    return obj


async def check_name_duplicate(model: object,
                               obj_name: str,
                               session: AsyncSession) -> None:
    crud = CRUDBase(model)
    obj_id = await crud.get_by_attribute(
        'name', obj_name, session
    )
    if obj_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Объект с таким именем уже существует'
        )
