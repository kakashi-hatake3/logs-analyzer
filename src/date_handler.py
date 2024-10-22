from datetime import datetime
from typing import Dict, Tuple

from src.enums import InputParameters


class DateHandler:
    """Обработчик даты."""

    def __init__(self, mapped_params: Dict[str, str], log_date: datetime):
        self.from_date = mapped_params.get(InputParameters.from_date, None)
        self.to_date = mapped_params.get(InputParameters.to_date, None)
        self.log_date = log_date.replace(tzinfo=None)

    def convert_iso_to_datetime(self) -> None:
        self.from_date, self.to_date = ConvertISOIntoDatetime(
            self.from_date, self.to_date
        ).get_dates()

    def is_within_timeframe(self) -> bool:
        """Конвертируем и возвращаем результат фильтрации."""
        self.convert_iso_to_datetime()
        return DateFilter(self.from_date, self.to_date).filter(self.log_date)


class ConvertISOIntoDatetime:
    """Переводим дату в другой формат."""

    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    def convert(self) -> None:
        """Переводим из ISO формата в datetime."""
        if self.from_date is not None:
            try:
                self.from_date = datetime.fromisoformat(self.from_date)
            except ValueError as e:
                print(e)
                exit()
        if self.to_date is not None:
            try:
                self.to_date = datetime.fromisoformat(self.to_date)
            except ValueError as e:
                print(e)
                exit()

    def get_dates(self) -> Tuple[datetime, datetime]:
        self.convert()
        return self.from_date, self.to_date


class DateFilter:
    """Проверяем дату на соответствие фильтру."""

    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    def filter(self, log_date) -> bool:
        """Проверяем попадает ли лог в указанный временной промежуток."""
        if self.from_date is None:
            lower_bound_check = True
        else:
            lower_bound_check = self.from_date <= log_date

        if self.to_date is None:
            upper_bound_check = True
        else:
            upper_bound_check = log_date <= self.to_date

        return lower_bound_check and upper_bound_check
