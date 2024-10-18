from typing import Dict

from src.nginx_parse import NginxLog
from src.wrong_input_error import WrongParameterNameError


class LogValueFilter:
    """Фильтр лога по значению какого-то параметра."""

    def __init__(self, mapped_params: Dict[str, str], log: NginxLog):
        self.log = log
        self.filter_field = mapped_params.get("filter-field", None)
        self.filter_value = mapped_params.get("filter-value", None)

    def _is_available(self) -> bool:
        """Проверяем есть ли оба параметра фильтра."""
        if self.filter_field is not None and self.filter_value is not None:
            return True
        return False

    def _is_filter_params_correctness(self) -> bool:
        """Проверяем правильно ли указано название параметра лога."""
        if self.filter_field in self.log.mapped_log.keys():
            return True
        return False

    def is_fits_the_filter(self) -> bool:
        """Проверяем удовлетворяет ли лог заданному фильтру."""
        if self._is_available():
            if self._is_filter_params_correctness():
                if self.filter_value in self.log.mapped_log[self.filter_field]:
                    return True
                return False
            else:
                raise WrongParameterNameError(self.filter_field)
