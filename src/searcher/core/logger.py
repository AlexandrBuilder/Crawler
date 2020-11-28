import logging
import sys
from logging import Handler, Logger as BaseLogger
from typing import List

from searcher.settings import Settings


class Logger(BaseLogger):

    def __init__(self, settings: Settings) -> None:
        super(Logger, self).__init__('app', settings.logger_level)
        self.handlers = self.get_handlers()

    @staticmethod
    def get_handlers() -> List[Handler]:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        return [handler]
