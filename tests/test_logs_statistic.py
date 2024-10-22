from src.logs_statistic import (
    RequestCountStatistic,
    MostCallableResourcesStatistic,
    MostFrequentStatusCodesStatistic,
    AverageResponseSizeStatistic,
    PercentileResponseSizeStatistic,
    MostFrequentIpAddressStatistic,
    MostFrequentAgentStatistic,
)

import numpy as np


class Log:
    def __init__(self, path, status_code, response_size, agent, ip):
        self.path = path
        self.status_code = status_code
        self.response_size = response_size
        self.agent = agent
        self.ip = ip


# Тест для RequestCountStatistic
def test_request_count_statistic():
    stat = RequestCountStatistic()
    log1 = Log("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = Log("/about", 404, 300, "agent2", "127.0.0.2")

    stat.update(log1)
    stat.update(log2)

    assert stat.get() == {"Кол-во запросов": 2}


# Тест для MostCallableResourcesStatistic
def test_most_callable_resources_statistic():
    stat = MostCallableResourcesStatistic()
    log1 = Log("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = Log("/about", 404, 300, "agent2", "127.0.0.2")
    log3 = Log("/home", 200, 400, "agent1", "127.0.0.3")

    stat.update(log1)
    stat.update(log2)
    stat.update(log3)

    assert stat.get() == {"Ресурсы": {"/home": 2, "/about": 1}}


# Тест для MostFrequentStatusCodesStatistic
def test_most_frequent_status_codes_statistic():
    stat = MostFrequentStatusCodesStatistic()
    log1 = Log("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = Log("/about", 404, 300, "agent2", "127.0.0.2")
    log3 = Log("/contact", 200, 400, "agent1", "127.0.0.3")

    stat.update(log1)
    stat.update(log2)
    stat.update(log3)

    assert stat.get() == {"Коды статуса": {200: 2, 404: 1}}


# Тест для AverageResponseSizeStatistic
def test_average_response_size_statistic():
    stat = AverageResponseSizeStatistic()
    log1 = Log("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = Log("/about", 404, 300, "agent2", "127.0.0.2")

    stat.update(log1)
    stat.update(log2)
    stat.calculate_average()

    assert stat.get() == {"Средний размер ответа": 400}


# Тест для MostFrequentAgentStatistic
def test_most_frequent_agent_statistic():
    stat = MostFrequentAgentStatistic()
    log1 = Log("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = Log("/about", 404, 300, "agent2", "127.0.0.2")
    log3 = Log("/contact", 200, 400, "agent1", "127.0.0.3")

    stat.update(log1)
    stat.update(log2)
    stat.update(log3)

    assert stat.get() == {"Самый частый агент": "agent1"}


# Тест для MostFrequentIpAddressStatistic
def test_most_frequent_ip_address_statistic():
    stat = MostFrequentIpAddressStatistic()
    log1 = Log("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = Log("/about", 404, 300, "agent2", "127.0.0.2")
    log3 = Log("/contact", 200, 400, "agent1", "127.0.0.1")

    stat.update(log1)
    stat.update(log2)
    stat.update(log3)

    assert stat.get() == {"Самый частый ip-адрес": "127.0.0.1"}


# Тест для PercentileResponseSizeStatistic
def test_percentile_response_size_statistic():
    stat = PercentileResponseSizeStatistic()
    log1 = Log("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = Log("/about", 404, 1000, "agent2", "127.0.0.2")
    log3 = Log("/contact", 200, 1500, "agent1", "127.0.0.3")
    log4 = Log("/help", 200, 2000, "agent1", "127.0.0.4")

    stat.update(log1)
    stat.update(log2)
    stat.update(log3)
    stat.update(log4)

    stat.calculate_percentile()

    assert stat.get() == {
        "95 перцентиль размера ответа": int(np.percentile([500, 1000, 1500, 2000], 95))
    }
