# Некоторые схемы вынесены в общий файл, чтобы избежать циклического импорта.

from typing import List

from app.schemas.pipeline import PipelineDB
from app.schemas.step import StepDB


class Pipeline_Steps(PipelineDB):
    steps: List[StepDB] = []


class Steps_Pipelines(StepDB):
    pipelines: List[PipelineDB] = []
