# Файл содержащий функции шагов пайплайнов
import json
from base64 import b64encode
from typing import List

import aiohttp
import cv2
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.car import Car


class Steps_funcs:

    file: bytes
    processed_image: bytes
    ml_response: List
    session: AsyncSession

    async def process_image(self) -> None:
        """Функция подготавливающая изображение
        к дальнейшей обработке."""
        imagenp = np.frombuffer(self.file, dtype=np.uint8)

        imagecv = cv2.imdecode(imagenp, cv2.IMREAD_COLOR)
        imagecv = cv2.resize(imagecv, (640, 640))

        norm_image = np.zeros((800, 800))
        norm_image = cv2.normalize(imagecv,
                                   norm_image,
                                   0,
                                   255,
                                   cv2.NORM_MINMAX)

        bytes_image = norm_image.tobytes()

        b64_image = b64encode(bytes_image)
        self.processed_image = b64_image

    async def ml_process_image(self) -> None:
        """Функция отправляющая запрос
        к внешнему сервису для обработки изображения."""
        url = settings.ml_service_url
        data = aiohttp.FormData()
        data.add_field(name='image',
                       value=self.processed_image)
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, data=data)
            self.ml_response = json.loads(await response.read())

    async def save_result(self):
        """Функция сохраняющая результат обработки
        изображения внешним сервисом."""
        session = self.session
        if len(self.ml_response) > 0:
            car_data = {
                'is_detected': True,
                'coordinates': (
                    f'[{self.ml_response[0]}, {self.ml_response[1]}]')
            }
            car = Car(**car_data)
            session.add(car)
            await session.commit()
            await session.refresh(car)
            return car
        car_data = {
            'is_detected': 1,
            'coordinates': None
        }
        car = Car(**car_data)
        session.add(car)
        await session.commit()
        await session.refresh(car)
        return car
