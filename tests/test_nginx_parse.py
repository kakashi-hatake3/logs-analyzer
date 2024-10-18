from datetime import datetime, timezone

import pytest

from src.nginx_parse import NginxLogParser, NginxLog

@pytest.fixture(scope="module")
def expected_dict_and_log():
    parser = NginxLogParser()
    log_line = '127.0.0.1 - - [21/May/2015:14:05:59 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0"'
    expected = {
        'ip': '127.0.0.1',
        'client_id': '-',
        'user_id': '-',
        'time_local': datetime(2015, 5, 21, 14, 5, 59, tzinfo=timezone.utc),
        'method': 'GET',
        'path': '/',
        'protocol': 'HTTP/1.1',
        'status_code': 200,
        'response_size': 612,
        'referrer': '-',
        'user_agent': 'Mozilla/5.0'
    }
    log: NginxLog = parser.parse_log_line(log_line)
    return expected, log


def test_nginx_parser_negative():
    parser = NginxLogParser()
    with pytest.raises(ValueError):
        parser.parse_log_line("aboba error")


def test_nginx_parser_ip(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['ip'] == log.ip


def test_nginx_parser_client_id(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['client_id'] == log.client_id


def test_nginx_parser_user_id(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['user_id'] == log.user_id


def test_nginx_parser_time_local(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['time_local'] == log.time_local


def test_nginx_parser_method(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['method'] == log.method


def test_nginx_parser_path(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['path'] == log.path


def test_nginx_parser_protocol(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['protocol'] == log.protocol


def test_nginx_parser_status_code(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['status_code'] == log.status_code


def test_nginx_parser_response_size(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['response_size'] == log.response_size


def test_nginx_parser_referrer(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['referrer'] == log.referrer


def test_nginx_parser_user_agent(expected_dict_and_log):
    expected, log = expected_dict_and_log
    assert expected['user_agent'] == log.user_agent
