from injector import singleton, provider, Module
from searcher.connection_managers.postgres_connection_manager import PostgresConnectionManager
from searcher.core.logger import Logger
from searcher.crawler import Crawler
from searcher.settings import Settings


class Container(Module):
    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()

    @singleton
    @provider
    def provide_logger(self, settings: Settings) -> Logger:
        return Logger(settings)

    @singleton
    @provider
    def provide_postgres_connection_manager(self, settings: Settings, logger: Logger) -> PostgresConnectionManager:
        return PostgresConnectionManager(settings, logger)

    @singleton
    @provider
    def provide_crawler(self, settings: Settings, logger: Logger) -> Crawler:
        return Crawler(settings, logger)
