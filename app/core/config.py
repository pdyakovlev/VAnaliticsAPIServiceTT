from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    app_title: str = 'П.Д.Яковлев тестовое'
    description: str = (
        'Сервис обработки изображений для платформы видеоаналитики')
    ml_service_url: str = 'http://127.0.0.1:8080/'

    class Config:
        env_file = '.env'


settings = Settings()
