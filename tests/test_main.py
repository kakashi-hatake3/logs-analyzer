from unittest.mock import MagicMock

import pytest

from src.main import main, run


def test_main() -> None:
    mock_mapper = MagicMock()
    mock_mapper.get_mapped_params.return_value = {'from': '2000-10-10', 'format': 'sdfs'}
    with pytest.raises(SystemExit):
        main()


def test_run():
    path = 'https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs'
    mapped_params = {'path': path}

    assert str(run(mapped_params)) == ("##############   markdown   ##############\n"
                                       "### {'Кол-во запросов': 51462}\n"
                                       "### {'Ресурсы': "
                                       "{'/downloads/product_1': 30285,"
                                       " '/downloads/product_2': 21104,"
                                       " '/downloads/product_3': 73}}\n"
                                       "### {'Самый частый агент': 'Debian APT-HTTP/1.3 (1.0.1ubuntu2)'}\n"
                                       "### {'Средний размер ответа': 659509}\n"
                                       "### {'Коды статуса':"
                                       " {304: 13330, 200: 4028, 404: 33876, 206: 186, 403: 38, 416: 4}}\n"
                                       "### {'Самый частый ip-адрес': '216.46.173.126'}\n"
                                       "### {'95 перцентиль размера ответа': 1768}\n")
