import pytest

from src.input_handler import InputMapper
from src.wrong_input_error import WrongInputError, WrongParameterNameError, WrongCountParametersError


@pytest.mark.parametrize(
    "params, expected",
    [
    (['main.py', '--path', 'scnd', '--from', 'ss'], {'path': 'scnd', 'from': 'ss'}),
    (['main.py', '-path', 'scnd', '--from', 'ss'], WrongInputError()),
    (['main.py', '--aboba', 'scnd', '--from', 'ss'], WrongParameterNameError('aboba')),
    (['main.py', '--aboba'], WrongCountParametersError(2)),
    ]
                         )
def test_input_mapper(params, expected):
    mapper = InputMapper()
    mapper.parameters = params
    assert mapper.get_mapped_params() == expected
