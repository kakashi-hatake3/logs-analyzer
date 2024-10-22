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
        CreateLog(self).create_log()

    def _filter_log(self) -> NginxLog | None:
        """Фильтруем лог по значению."""
        return FilterLog(self).filter_log()

    def _is_date_filter(self) -> bool:
        """Проверяем проходит ли лог по времени."""
        return DateFilter(self).is_date_filter()

    def get_log(self) -> NginxLog | None:
        """Возвращаем лог."""
        self._create_log()
        if self._is_date_filter():
            return self._filter_log()


class DateFilter:
    """Фильтруем по времени."""

    def __init__(self, processor: ProcessLog):
        self.processor = processor

    def is_date_filter(self) -> bool:
        """Проверяем проходит ли лог по времени."""
        date_handler = DateHandler(
            self.processor.mapped_params, self.processor.log.time_local
        )
        return date_handler.is_within_timeframe()


class CreateLog:
    """Создаем лог."""

    def __init__(self, processor: ProcessLog):
        self.processor = processor

    def create_log(self) -> None:
        """Создаем лог."""
        try:
            self.processor.log = NginxLogParser().parse_log_line(
                self.processor.log_line
            )
        except ValueError as e:
            print(e)
            exit()


class FilterLog:

    def __init__(self, processor: ProcessLog):
        self.processor = processor

    def filter_log(self) -> NginxLog | None:
        """Фильтруем лог по значению."""
        filter = LogValueFilter(self.processor.mapped_params, self.processor.log)
        # если один раз обработали ошибку неправильного имени параметра,
        # то в дальнейших логах не проверяем ее,
        # потому что параметры переданные пользователем меняться не будут
        if not self.processor.is_error_handled:
            try:
                if filter.is_fits_filter_first_check():
                    self.processor.is_error_handled = True
                    return self.processor.log
            except WrongParameterNameError as e:
                print(e)
                exit()
        else:
            if filter.is_fits_filter():
                return self.processor.log
