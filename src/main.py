import logging
import platform

from src.format_handler import FormatHandler
from src.logs_handler import LogsHandler, PathHandler
from src.input_handler import InputMapper
from src.logs_statistic import RequestCountStatistic, MostCallableResourcesStatistic, MostFrequentAgentStatistic, \
    AverageResponseSizeStatistic, MostFrequentStatusCodesStatistic, MostFrequentIpAddressStatistic, \
    PercentileResponseSizeStatistic
from src.report import MarkdownReport, AdocReport
from src.wrong_input_error import WrongParameterNameError

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def get_mapped_params():
    mapper = InputMapper()
    mapped_params = mapper.get_mapped_params()
    return mapped_params


def run(mapped_params):
    try:
        report_format = FormatHandler(mapped_params).get_format()
    except WrongParameterNameError as e:
        print(e)
        exit()

    path_handler = PathHandler(mapped_params)

    data_handler = LogsHandler(path_handler)

    stats = [
        RequestCountStatistic(),
        MostCallableResourcesStatistic(),
        MostFrequentAgentStatistic(),
        AverageResponseSizeStatistic(),
        MostFrequentStatusCodesStatistic(),
        MostFrequentIpAddressStatistic(),
        PercentileResponseSizeStatistic(),
    ]

    if report_format == 'adoc':
        report = AdocReport()
    else:
        report = MarkdownReport()

    for log in data_handler.get_logs():
        for statistic in stats:
            statistic.update(log)
    for statistic in stats:
        report.add_statistic(statistic.get())

    report.generate_report()
    return report


def main() -> None:
    logger.info(platform.python_version())

    mapped_params = get_mapped_params()
    print(run(mapped_params))


if __name__ == "__main__":
    main()
