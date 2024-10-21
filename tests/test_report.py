from src.logs_statistic import RequestCountStatistic, MostFrequentStatusCodesStatistic
from src.report import Report


class LogTest:
    def __init__(self, path, status_code, response_size, agent, ip):
        self.path = path
        self.status_code = status_code
        self.response_size = response_size
        self.agent = agent
        self.ip = ip


# Тест для класса Report
def test_report_add_statistic():
    report = Report()
    stat = RequestCountStatistic()
    log = LogTest("/home", 200, 500, "agent1", "127.0.0.1")

    stat.update(log)
    report.add_statistic(stat)

    # Убедимся, что статистика добавлена в отчет
    assert len(report.statistics) == 1
    assert report.statistics[0] == stat


def test_report_generate_markdown():
    report = Report()
    stat = RequestCountStatistic()
    log1 = LogTest("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = LogTest("/about", 404, 300, "agent2", "127.0.0.2")

    stat.update(log1)
    stat.update(log2)
    report.add_statistic(stat)

    markdown_output = report.generate_report('markdown')

    # Ожидаемый вывод в формате markdown
    expected_output = (
        "### Кол-во запросов\n"
        "- **Value:** 2\n\n"
    )

    assert markdown_output == expected_output


def test_report_generate_adoc():
    report = Report()
    stat = RequestCountStatistic()
    log1 = LogTest("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = LogTest("/about", 404, 300, "agent2", "127.0.0.2")

    stat.update(log1)
    stat.update(log2)
    report.add_statistic(stat)

    adoc_output = report.generate_report('adoc')

    # Ожидаемый вывод в формате adoc
    expected_output = (
        "== Кол-во запросов\n"
        "* Value: 2\n\n"
    )

    assert adoc_output == expected_output


def test_report_none_format():
    report = Report()
    stat = RequestCountStatistic()
    log1 = LogTest("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = LogTest("/about", 404, 300, "agent2", "127.0.0.2")

    stat.update(log1)
    stat.update(log2)
    report.add_statistic(stat)

    markdown_output = report.generate_report(None)

    # Ожидаемый вывод в формате markdown
    expected_output = (
        "### Кол-во запросов\n"
        "- **Value:** 2\n\n"
    )

    assert markdown_output == expected_output


# Тест для нескольких статистик
def test_report_multiple_statistics():
    report = Report()

    # Статистика количества запросов
    request_count_stat = RequestCountStatistic()
    log1 = LogTest("/home", 200, 500, "agent1", "127.0.0.1")
    log2 = LogTest("/about", 404, 300, "agent2", "127.0.0.2")
    request_count_stat.update(log1)
    request_count_stat.update(log2)

    # Статистика кодов состояния
    status_code_stat = MostFrequentStatusCodesStatistic()
    status_code_stat.update(log1)
    status_code_stat.update(log2)

    # Добавляем обе статистики в отчет
    report.add_statistic(request_count_stat)
    report.add_statistic(status_code_stat)

    # Ожидаемый отчет в формате markdown
    markdown_output = report.generate_report('markdown')
    expected_output = (
        "### Кол-во запросов\n"
        "- **Value:** 2\n\n"
        "### 200\n"
        "- **Value:** 1\n\n"
        "### 404\n"
        "- **Value:** 1\n\n"
    )

    assert markdown_output == expected_output
