from typing import Callable

from src.date_handler import DateHandler
from src.log_value_filter import LogValueFilter
from src.nginx_parse import NginxLog, NginxLogParser
from src.wrong_input_error import WrongParameterNameError


class ProcessLog:
    """Создаем лог и проверяем его на фильтры."""

    def __init__(self, log_line, mapped_params):
        self.log_line = log_line
        self.mapped_params = mapped_params
        self.log: NginxLog | None = None
        self.is_error_handled = False


    def _create_log(self) -> None:
        """Создаем лог."""
        try:
            self.log = NginxLogParser().parse_log_line(self.log_line)
        except ValueError as e:
            print(e)
            exit()


    def _filter_log(self) -> NginxLog | None:
        """Фильтруем лог по значению."""
        filter = LogValueFilter(self.mapped_params, self.log)
        #если один раз обработали ошибку неправильного имени параметра,
        # то в дальнейших логах не проверяем ее,
        # потому что параметры переданные пользователем меняться не будут
        if not self.is_error_handled:
            try:
                if filter.is_fits_the_filter():
                    self.is_error_handled = True
                    return self.log
            except WrongParameterNameError as e:
                print(e)
                exit()
        else:
            if filter.filter():
                return self.log

    def _is_date_filter(self) -> bool:
        """Проверяем проходит ли лог по времени."""
        date_handler = DateHandler(self.mapped_params, self.log.time_local)
        return date_handler.is_within_timeframe()

    def get_log(self) -> Callable[[], NginxLog | None]:
        """Возвращаем лог."""
        self._create_log()
        if self._is_date_filter():
            return self._filter_log
