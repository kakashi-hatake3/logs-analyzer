import pytest
from datetime import datetime

from src.date_handler import DateHandler


@pytest.mark.parametrize(
    "params, expected",
    [
        ({'from': '2000-10-10', 'format': 'adoc'}, True),
        ({'to': '2020-10-10', 'format': 'adoc'}, True),
        ({'from': '2000-10-10', 'to': '2020-10-10', 'format': 'adoc'}, True),
        ({'format': 'adoc'}, True),
        ({'from': '2020-10-10', 'format': 'adoc'}, False),
        ({'to': '2010-10-10', 'format': 'adoc'}, False),
        ({'from': '2020-10-10', 'to': '2030-10-10', 'format': 'adoc'}, False),
        ({'from': '2030-10-10', 'to': '2020-10-10', 'format': 'adoc'}, False),
    ]
                         )
def test_date_handler(params, expected):
    date_handler = DateHandler(params, datetime(2012, 4, 1))
    assert date_handler.is_within_timeframe() == expected
