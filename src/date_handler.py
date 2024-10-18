from datetime import datetime
from typing import Dict


class DateHandler:
    """Обработчик даты."""

    def __init__(self, mapped_params: Dict[str, str], nginx_date: datetime):
        self.from_date = mapped_params.get("from", None)
        self.to_date = mapped_params.get("to", None)
        self.nginx_date = nginx_date

    def _convert_iso_to_datetime(self):
        if self.from_date:
            self.from_date = datetime.fromisoformat(self.from_date)
        if self.to_date:
            self.to_date = datetime.fromisoformat(self.to_date)

    def is_within_timeframe(self) -> bool:
        self._convert_iso_to_datetime()

        if self.from_date is None:
            lower_bound_check = True
        else:
            lower_bound_check = self.from_date <= self.nginx_date

        if self.to_date is None:
            upper_bound_check = True
        else:
            upper_bound_check = self.nginx_date <= self.to_date

        return lower_bound_check and upper_bound_check
