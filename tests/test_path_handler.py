from src.logs_handler import PathHandler

import pytest

from src.wrong_input_error import WrongPathError


@pytest.mark.parametrize(
    "params, expected",
    [
        ({'path': 'scnd', 'format': 'adoc'}, 'local'),
        ({'path': 'https://scnd', 'format': 'adoc'}, 'url'),
    ]
                         )
def test_path_type_positive(params, expected):
    path_handler = PathHandler(params)
    path_handler.define_path_type()
    assert path_handler.path_type == expected


def test_path_type_negative():
    path_handler = PathHandler({'format': 'adoc'})
    with pytest.raises(WrongPathError):
        path_handler.define_path_type()
