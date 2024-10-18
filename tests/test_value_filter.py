import pytest

from src.log_value_filter import LogValueFilter
from src.nginx_parse import NginxLog, NginxLogParser
from src.wrong_input_error import WrongParameterNameError


@pytest.fixture(scope="module")
def get_log():
    log_line = '127.0.0.1 - - [21/May/2015:14:05:59 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0"'
    log = NginxLogParser().parse_log_line(log_line)
    return log


@pytest.mark.parametrize(
    "params, expected",
    [
        ({'from': '2000-10-10', 'format': 'adoc', 'filter-field': 'method', 'filter-value': 'GET'}, True),
        ({'from': '2000-10-10', 'format': 'adoc', 'filter-field': 'method', 'filter-value': 'POST'}, False),
        ({'from': '2000-10-10', 'format': 'adoc', 'filter-value': 'GET'}, None),
        ({'from': '2000-10-10', 'format': 'adoc'}, None),
    ]
                         )
def test_value_filter(get_log, params, expected):
    log = get_log
    log_filter = LogValueFilter(params, log)
    assert log_filter.is_fits_the_filter() == expected


def test_value_filter_error(get_log):
    log = get_log
    params = {'from': '2000-10-10', 'format': 'adoc', 'filter-field': 'aboba', 'filter-value': 'POST'}
    log_filter = LogValueFilter(params, log)
    with pytest.raises(WrongParameterNameError):
        log_filter.is_fits_the_filter()
