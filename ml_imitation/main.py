import random
from typing import Annotated, List

from fastapi import FastAPI, File

app = FastAPI(title='Имитация работы ML модели')


@app.post('/')
async def get_car_from_image(image: Annotated[bytes, File()]) -> List:
    """Получить координаты авто из изображения."""
    rnd = random.random()
    if rnd > 0.5:
        w = random.randint(10, 50)
        h = random.randint(10, 50)
        top_left_x = random.randint(0, 650-w)
        top_left_y = random.randint(0, 650-h)
        conf = random.random()
        label = 1
        resp = [top_left_x, top_left_y, w, h, conf, label]
        return (resp)
    return ([])
