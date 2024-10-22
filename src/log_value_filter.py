from typing import Dict

from src.enums import LogFields
from src.nginx_parse import NginxLog
from src.wrong_input_error import WrongParameterNameError


class LogValueFilter:
    """Фильтр лога по значению какого-то параметра."""

    def __init__(self, mapped_params: Dict[str, str], log: NginxLog):
        self.log = log
        self.filter_field = mapped_params.get("filter-field", None)
        self.filter_value = mapped_params.get("filter-value", None)
        self.both_is_none = False

    def is_fits_filter_first_check(self) -> bool:
        """Проверяем на ошибки."""
        check_filter = CheckFilterValuesCorrectness(self.filter_field, self.filter_value, self.both_is_none)
        if check_filter.is_available():
            self.both_is_none = check_filter.both_is_none
            if self.both_is_none:
                return True
            if check_filter.is_filter_params_correctness():
                return self.is_fits_filter()
            else:
                raise WrongParameterNameError(self.filter_field)

    def is_fits_filter(self) -> bool:
        """Проверяем удовлетворяет ли лог заданному фильтру."""
        if self.both_is_none:
            return True
        if self.filter_value in str(self.log.mapped_log[self.filter_field]):
            return True
        return False


class CheckFilterValuesCorrectness:

    def __init__(self, filter_field, filter_value, both_is_none):
        self.both_is_none = both_is_none
        self.filter_field = filter_field
        self.filter_value = filter_value
        self.log_fields = [
            LogFields.ip,
            LogFields.client_id,
            LogFields.user_id,
            LogFields.time_local,
            LogFields.method,
            LogFields.path,
            LogFields.protocol,
            LogFields.status_code,
            LogFields.response_size,
            LogFields.referrer,
            LogFields.agent,
        ]

    def is_available(self) -> bool:
        """Проверяем есть ли оба параметра фильтра."""
        if isinstance(self.filter_field, type(self.filter_value)):
            if self.filter_value is None and self.filter_field is None:
                self.both_is_none = True
            return True
        return False

    def is_filter_params_correctness(self) -> bool:
        """Проверяем правильно ли указано название параметра лога."""
        if self.filter_field in self.log_fields:
            return True
        return False
