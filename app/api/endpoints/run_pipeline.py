from typing import List, Union

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.pipeline import pipeline_crud
from app.schemas.car import CarSchema
from app.steps_funcs.funcs import Steps_funcs

router = APIRouter(prefix='/process_image', tags=['process_image'])


@router.post('', response_model=Union[CarSchema, str])
async def process_image(
    pipeline_id: int,
    file: UploadFile = None,
        session: AsyncSession = Depends(get_async_session)) -> str:
    """Запустить пайплайн."""
    pipeline = await pipeline_crud.get_pipeline_w_steps(pipeline_id, session)
    steps_funcs = Steps_funcs()
    funcs: List[str] = []
    for step in pipeline.steps:
        funcs.append(step.func)
    if file is not None:
        steps_funcs.file = file.file.read()
        steps_funcs.session = session
        for func in funcs:
            if func in dir(steps_funcs):
                step_func = getattr(steps_funcs, func)
                resp = await step_func()
        if resp is not None:
            return resp
    return ('Сделано всё, что возможно.')
