from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import check_name_duplicate, check_obj_exists
from app.core.db import get_async_session
from app.crud.step import step_crud
from app.models.step import Step
from app.schemas.common import Steps_Pipelines
from app.schemas.step import StepCreate, StepDB, StepUpdate

router = APIRouter(prefix='/steps', tags=['Steps'])


@router.get('/',
            response_model=list[StepDB],
            response_model_exclude_none=True)
async def get_all_steps(
    session: AsyncSession = Depends(get_async_session)
):
    """Получить все шаги пайплайнов из базы."""
    return await step_crud.get_multi(session=session)


@router.post('/',
             response_model=StepDB,
             response_model_exclude_none=True)
async def create_new_step(
        step: StepCreate,
        session: AsyncSession = Depends(get_async_session)):
    """Создать новый шаг."""
    await check_name_duplicate(Step, step.name, session)
    new_step = await step_crud.create(step, session)
    return new_step


@router.get('/{step_id}',
            response_model=Steps_Pipelines,
            response_model_exclude_none=True)
async def get_step_full_info(
    step_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получить информацию к каким пайплайнам привязан шаг."""
    return await step_crud.get_step_w_pipelines(step_id, session=session)


@router.patch('/{step_id}',
              response_model=StepDB,
              response_model_exclude_none=True)
async def partially_update_step(step_id: int,
                                upd_data: StepUpdate,
                                session: AsyncSession = Depends(
                                    get_async_session)):
    """Редактировать шаг."""
    step = await check_obj_exists(Step, step_id, session)
    if upd_data.name is not None:
        await check_name_duplicate(Step, upd_data.name, session)

    step = await step_crud.update(step, upd_data, session)
    return step


@router.delete('/{step_id}',
               response_model=StepDB,
               response_model_exclude_none=True)
async def remove_step(step_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    """Удалить шаг."""
    step = await check_obj_exists(Step, step_id, session)
    step = await step_crud.remove(step, session)
    return step
