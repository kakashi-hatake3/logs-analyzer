from abc import abstractmethod, ABC
from typing import Dict
import numpy as np

from src.nginx_parse import NginxLog


class UpdateStatistic(ABC):

    @abstractmethod
    def update(self, log: NginxLog) -> None:
        pass


class GetStatistic(ABC):

    @abstractmethod
    def get(self) -> Dict:
        pass


class RequestCountStatistic(UpdateStatistic, GetStatistic):

    def __init__(self):
        self.count = 0

    def update(self, log):
        self.count += 1

    def get(self):
        return {'Кол-во запросов': self.count}


class MostCallableResourcesStatistic(UpdateStatistic, GetStatistic):

    def __init__(self):
        self.resources = {}

    def update(self, log):
        if log.path not in self.resources.keys():
            self.resources[log.path] = 0
        self.resources[log.path] += 1

    def get(self):
        return self.resources


class MostFrequentStatusCodesStatistic(UpdateStatistic, GetStatistic):

    def __init__(self):
        self.status_codes = {}

    def update(self, log):
        if log.status_code not in self.status_codes.keys():
            self.status_codes[log.status_code] = 0
        self.status_codes[log.status_code] += 1

    def get(self):
        return self.status_codes


class AverageResponseSizeStatistic(UpdateStatistic, GetStatistic):

    def __init__(self):
        self.sizes = []
        self.average_size = 0

    def calculate_average(self):
        self.average_size = sum(self.sizes) / len(self.sizes)

    def update(self, log):
        self.sizes.append(log.response_size)

    def get(self):
        return {'Средний размер ответа': self.average_size}


class MostFrequentAgentStatistic(UpdateStatistic, GetStatistic):

    def __init__(self):
        self.agents = {}
        self.agent = ''

    def compute_agent(self):
        max_meeted_agent_and_count = ('', 0)
        for agent in self.agents.keys():
            if self.agents[agent] > max_meeted_agent_and_count[1]:
                max_meeted_agent_and_count = agent, self.agents[agent]
        self.agent = max_meeted_agent_and_count[0]

    def update(self, log):
        if log.agent not in self.agents.keys():
            self.agents[log.agent] = 0
        self.agents[log.agent] += 1

    def get(self):
        self.compute_agent()
        return {'Самый частый агент': self.agent}


class MostFrequentIpAddressStatistic(UpdateStatistic, GetStatistic):

    def __init__(self):
        self.ips = {}
        self.ip = ''

    def compute_ip_count(self):
        ip_and_count = ('', 0)
        for ip in self.ips.keys():
            if self.ips[ip] > ip_and_count[1]:
                ip_and_count = ip, self.ips[ip]
        self.ip = ip_and_count[0]

    def update(self, log):
        if log.ip not in self.ips.keys():
            self.ips[log.ip] = 0
        self.ips[log.ip] += 1

    def get(self):
        self.compute_ip_count()
        return {'Самый частый ip-адрес': self.ip}


class PercentileResponseSizeStatistic(UpdateStatistic, GetStatistic):

    def __init__(self):
        self.sizes = []
        self.percentile = 0

    def calculate_percentile(self):
        self.percentile = np.percentile(self.sizes, 95)

    def update(self, log):
        self.sizes.append(log.response_size)

    def get(self):
        self.calculate_percentile()
        return {'95 перцентиль размера ответа': self.percentile}
