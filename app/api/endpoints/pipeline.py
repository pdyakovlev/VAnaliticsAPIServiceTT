from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import (check_name_duplicate, check_obj_exists,
                           create_first_pipeline)
from app.core.db import get_async_session
from app.crud.pipeline import pipeline_crud
from app.models.pipeline import Pipeline
from app.models.step import Step
from app.schemas.common import Pipeline_Steps
from app.schemas.pipeline import PipelineCreate, PipelineDB, PipelineUpdate

router = APIRouter(prefix='/pipelines', tags=['Pipelines'])


@router.get('/set_data')
async def create_min_data(
    session: AsyncSession = Depends(get_async_session)
):
    """Автоматически добавить пайплайн детекции авто и его шаги."""
    await create_first_pipeline(session)
    return 'Done!'


@router.get('/',
            response_model=list[PipelineDB],
            response_model_exclude_none=True)
async def get_all_pipelines(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить все пайплайны из базы."""
    return await pipeline_crud.get_multi(session=session)


@router.post('/',
             response_model=PipelineDB,
             response_model_exclude_none=True)
async def create_new_pipeline(
        pipeline: PipelineCreate,
        session: AsyncSession = Depends(get_async_session)):
    """Создать пайплайн."""
    await check_name_duplicate(Pipeline, pipeline.name, session)
    new_pipeline = await pipeline_crud.create(pipeline, session)
    return new_pipeline


@router.patch('/{pipeline_id}',
              response_model=PipelineDB,
              response_model_exclude_none=True)
async def partially_update_pipeline(pipeline_id: int,
                                    upd_data: PipelineUpdate,
                                    session: AsyncSession = Depends(
                                        get_async_session)):
    """Редактировать пайплайн."""
    pipeline = await check_obj_exists(Pipeline, pipeline_id, session)
    if upd_data.name is not None:
        await check_name_duplicate(Pipeline, upd_data.name, session)

    pipeline = await pipeline_crud.update(pipeline, upd_data, session)
    return pipeline


@router.patch('/{pipeline_id}/add_step/',
              response_model=Pipeline_Steps,
              response_model_exclude_none=True)
async def add_step_to_pipeline(pipeline_id: int,
                               step_id: int,
                               session: AsyncSession = Depends(
                                   get_async_session)):
    """Добавить шаг к пайплайну."""
    await check_obj_exists(Pipeline, pipeline_id, session)
    pipeline = await pipeline_crud.get_pipeline_w_steps(
        pipeline_id, session)
    step = await check_obj_exists(Step, step_id, session)
    step_data = {'step': step}
    pipeline = await pipeline_crud.add_step(pipeline, step_data, session)
    return pipeline


@router.get('/{pipeline_id}',
            response_model=Pipeline_Steps,
            response_model_exclude_none=True)
async def get_pipeline_full_info(
    pipeline_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получить информацию о шагах пайплайна."""
    await check_obj_exists(Pipeline, pipeline_id, session)
    return await pipeline_crud.get_pipeline_w_steps(
        pipeline_id, session)


@router.delete('/{pipeline_id}',
               response_model=PipelineDB,
               response_model_exclude_none=True)
async def remove_pipeline(pipeline_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    """Удалить пайплайн."""
    pipeline = await check_obj_exists(Pipeline, pipeline_id, session)
    pipeline = await pipeline_crud.remove(pipeline, session)
    return pipeline
