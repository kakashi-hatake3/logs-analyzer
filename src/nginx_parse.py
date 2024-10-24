import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from src.enums import LogFields

@dataclass
class NginxLog:
    ip: str
    client_id: str
    user_id: str
    time_local: datetime
    method: str
    path: str
    protocol: str
    status_code: int
    response_size: int
    referrer: str
    agent: str
    mapped_log: Dict[str, str | int]


class NginxLogParser:
    # Регулярное выражение для парсинга строки лога
    log_pattern = re.compile(
        r"(?P<ip>\S+) "
        r"(?P<client_id>\S+) "
        r"(?P<user_id>\S+) "
        r"\[(?P<time_local>[^\]]+)\] "
        r'"(?P<method>\S+) '
        r"(?P<path>\S+) "
        r'(?P<protocol>[^"]+)" '
        r"(?P<status_code>\d{3}) "
        r"(?P<response_size>\S+) "
        r'"(?P<referrer>[^"]*)" '
        r'"(?P<agent>[^"]*)"'
    )

    def parse_log_line(self, log_line):
        match = self.log_pattern.match(log_line)
        if match:
            data = match.groupdict()

            time_local = self.parse_time(data[LogFields.time_local])

            # Если размер ответа '-', то это означает, что размер неизвестен, заменим на 0
            data[LogFields.response_size] = (
                int(data[LogFields.response_size])
                if data[LogFields.response_size] != "-"
                else 0
            )

            data[LogFields.status_code] = int(data[LogFields.status_code])

            return NginxLog(
                ip=data[LogFields.ip],
                client_id=data[LogFields.client_id],
                user_id=data[LogFields.user_id],
                time_local=time_local,
                method=data[LogFields.method],
                path=data[LogFields.path],
                protocol=data[LogFields.protocol],
                status_code=data[LogFields.status_code],
                response_size=data[LogFields.response_size],
                referrer=data[LogFields.referrer],
                agent=data[LogFields.agent],
                mapped_log=data,
            )
        else:
            raise ValueError(f"Лог не соответствует формату: {log_line}")

    def parse_time(self, time_str):
        """Парсинг времени формата Nginx в объект datetime."""
        nginx_time_format = "%d/%b/%Y:%H:%M:%S %z"
        return datetime.strptime(time_str, nginx_time_format)
