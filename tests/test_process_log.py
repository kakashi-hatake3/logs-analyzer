from unittest.mock import patch, MagicMock

import pytest
from pytest_mock import mocker

from src.nginx_parse import NginxLogParser
from src.process_log import ProcessLog


@pytest.fixture
def mapped_params():
    """Фикстура для параметров, маппинга."""
    return {'from': '2000-10-10', 'format': 'adoc', 'filter-field': 'method', 'filter-value': 'GET'}


@pytest.fixture
def none_mapped_params():
    """Фикстура для параметров, маппинга."""
    return {'from': '2000-10-10', 'format': 'adoc'}


@pytest.fixture
def wrong_mapped_params():
    """Фикстура для параметров, маппинга."""
    return {'from': '2020-10-10', 'format': 'adoc', 'filter-field': 'aboba', 'filter-value': 'GET'}


@pytest.fixture
def log_line():
    """Фикстура для строки лога."""
    return '127.0.0.1 - - [21/May/2015:14:05:59 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0"'


@pytest.fixture
def nginx_log(log_line):
    """Фикстура для создания тестового NginxLog."""
    return NginxLogParser().parse_log_line(log_line)


@pytest.fixture
def mock_log_value_filter():
    return mocker.patch('src.log_value_filter.LogValueFilter')


def test_create_log_success(log_line, mapped_params, nginx_log):
    """Тест успешного создания лога."""
    process_log = ProcessLog(log_line, mapped_params)
    with patch.object(NginxLogParser, 'parse_log_line', return_value=nginx_log):
        process_log._create_log()
        assert process_log.log.mapped_log == nginx_log.mapped_log


def test_create_log_failure(log_line, mapped_params):
    """Тест ошибки при создании лога (ValueError)."""
    process_log = ProcessLog(log_line, mapped_params)
    with patch.object(NginxLogParser, 'parse_log_line', side_effect=ValueError("Invalid log line")):
        with pytest.raises(SystemExit):  # Ожидаем, что программа завершится с exit()
            process_log._create_log()


def test_filter_log_none(log_line, none_mapped_params):
    """Тест None фильтрации лога."""
    processor = ProcessLog(log_line, none_mapped_params)
    processor._create_log()
    assert processor._filter_log() is None


def test_filter_log_success(log_line, mapped_params, nginx_log):
    """Тест успешной фильтрации лога."""
    processor = ProcessLog(log_line, mapped_params)
    processor._create_log()
    assert processor._filter_log().mapped_log == nginx_log.mapped_log


def test_filter_log_wrong_param_name_error(log_line, wrong_mapped_params):
    """Тест обработки ошибки неверного имени параметра."""
    processor = ProcessLog(log_line, wrong_mapped_params)
    processor._create_log()
    with pytest.raises(SystemExit):
        processor._filter_log()


def test_is_date_filter_within_timeframe(log_line, mapped_params):
    """Тест, что лог проходит фильтр по времени."""
    processor = ProcessLog(log_line, mapped_params)
    processor._create_log()
    assert processor._is_date_filter() == True

def test_is_date_filter_without_timeframe(log_line, wrong_mapped_params):
    """Тест, что лог не проходит фильтр по времени."""
    processor = ProcessLog(log_line, wrong_mapped_params)
    processor._create_log()
    assert processor._is_date_filter() == False
