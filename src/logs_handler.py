from typing import Generator

from src.enums import PathTypes
import requests

from src.nginx_parse import NginxLog
from src.path_handler import PathHandler
from src.process_log import ProcessLog
from src.wrong_input_error import WrongFileError, WrongHtmlError, WrongPathError


class LogsHandler:
    """Берем данные по полученному пути."""

    def __init__(self, path_handler: PathHandler):
        self.path_handler = path_handler
        self._define_path()
        self.path_type = self.path_handler.path_type
        self.path = self.path_handler.file_path
        self.mapped_params = self.path_handler.mapped_params
        self.log: NginxLog | None = None

    def _define_path(self) -> None:
        try:
            self.path_handler.define_path_type()
        except WrongPathError as e:
            print(e)
            exit()

    def _get_local_logs(self) -> NginxLog | None:
        """Получаем логи локально."""
        try:
            with open(self.path, 'r') as f:
                return self._generate_log(f.readlines())
        except OSError:
            print(WrongFileError())
            exit()

    def _get_remote_logs(self) -> NginxLog | None:
        """Получаем логи по URL."""
        response = requests.get(self.path, stream=True)
        if response.status_code == 200:
            try:
                return self._generate_log(response.text.splitlines())
            except WrongHtmlError as e:
                print(e)
                exit()
        else:
            print(WrongFileError())
            exit()

    def _generate_log(self, logs) -> NginxLog:
        """Возвращаем логи по-одному."""
        for line in logs:
            processor = ProcessLog(line, self.mapped_params)
            self.log = processor.get_log()
            if self.log is not None:
                yield self.log

    def get_logs(self) -> Generator | None:
        """Выбираем каким способом берем логи."""
        if self.path_type == PathTypes.url.value:
            return self._get_remote_logs()
        elif self.path_type == PathTypes.local.value:
            return self._get_local_logs()
