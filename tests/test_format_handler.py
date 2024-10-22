import pytest

from src.format_handler import FormatHandler
from src.wrong_input_error import WrongParameterNameError


@pytest.mark.parametrize(
    "params, expected",
    [
        ({"path": "scnd", "format": "adoc"}, "adoc"),
        ({"path": "scnd", "format": "aboba"}, WrongParameterNameError("aboba")),
        ({"path": "scnd", "from": "ss"}, None),
    ],
)
def test_format_handler(params, expected):
    format_handler = FormatHandler(params)
    assert format_handler.get_format() == expected
