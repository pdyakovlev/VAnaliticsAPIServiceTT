from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.step import Step


class StepCRUD(CRUDBase):
    async def get_step_w_pipelines(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(Step).where(Step.id == obj_id).options(
                selectinload(Step.pipelines)))
        return db_obj.scalars().first()


step_crud = StepCRUD(Step)
