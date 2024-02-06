from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.pipeline import Pipeline


class PipelineCRUD(CRUDBase):
    async def add_step(
            self,
            pipeline: Pipeline,
            step_data,
            session: AsyncSession,
    ):
        pipeline.steps.append(step_data['step'])
        session.add(pipeline)
        await session.commit()
        await session.refresh(pipeline)
        return pipeline

    async def get_pipeline_w_steps(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(Pipeline).where(Pipeline.id == obj_id).options(
                selectinload(Pipeline.steps)))
        return db_obj.scalars().first()


pipeline_crud = PipelineCRUD(Pipeline)
