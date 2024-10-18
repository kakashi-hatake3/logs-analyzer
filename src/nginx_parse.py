import re
from datetime import datetime
from typing import Dict


class NginxLog:
    def __init__(self, ip, client_id, user_id, time_local, method, path, protocol, status_code, response_size, referrer,
                 agent, mapped_log: Dict[str, str | int]):
        self.ip = ip
        self.client_id = client_id
        self.user_id = user_id
        self.time_local = time_local
        self.method = method
        self.path = path
        self.protocol = protocol
        self.status_code = status_code
        self.response_size = response_size
        self.referrer = referrer
        self.agent = agent
        self.mapped_log = mapped_log


class NginxLogParser:
    # Регулярное выражение для парсинга строки лога
    log_pattern = re.compile(
        r'(?P<ip>\S+) ' 
        r'(?P<client_id>\S+) '  
        r'(?P<user_id>\S+) ' 
        r'\[(?P<time_local>[^\]]+)\] ' 
        r'"(?P<method>\S+) '  
        r'(?P<path>\S+) '  
        r'(?P<protocol>[^"]+)" ' 
        r'(?P<status_code>\d{3}) ' 
        r'(?P<response_size>\S+) '  
        r'"(?P<referrer>[^"]*)" ' 
        r'"(?P<agent>[^"]*)"'
    )

    def parse_log_line(self, log_line):
        match = self.log_pattern.match(log_line)
        if match:
            data = match.groupdict()

            time_local = self.parse_time(data['time_local'])

            # Если размер ответа '-', то это означает, что размер неизвестен, заменим на None
            data['response_size'] = int(data['response_size']) if data['response_size'] != '-' else None

            data['status_code'] = int(data['status_code'])

            # Создаем объект NginxLogEntry
            return NginxLog(
                ip=data['ip'],
                client_id=data['client_id'],
                user_id=data['user_id'],
                time_local=time_local,
                method=data['method'],
                path=data['path'],
                protocol=data['protocol'],
                status_code=data['status_code'],
                response_size=data['response_size'],
                referrer=data['referrer'],
                agent=data['agent'],
                mapped_log=data
            )
        else:
            raise ValueError(f"Лог не соответствует формату: {log_line}")

    def parse_time(self, time_str):
        """Парсинг времени формата Nginx в объект datetime."""
        nginx_time_format = "%d/%b/%Y:%H:%M:%S %z"
        return datetime.strptime(time_str, nginx_time_format)
