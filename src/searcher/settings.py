from pydantic import BaseSettings
import logging


class Settings(BaseSettings):
    logger_level = logging.INFO

    postgres_host: str
    postgres_port: str
    postgres_username: str
    postgres_password: str
    postgres_db: str

    root_url: str = 'https://habr.com/ru/'
    max_depth: int = 1
    max_request_count: int = 30


    @property
    def postgres_dsn(self) -> str:
        return 'postgres://{}:{}@{}:{}/{}'.format(
            self.postgres_username,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_db,
        )

    class Config:
        env_file = '.env'
