import pytest

from src.logs_handler import LogsHandler
from src.path_handler import PathHandler


@pytest.mark.parametrize(
    "params",
    (
        {"from": "ss", "path": "aboba"},
        {"from": "ss"},
        {"path": "https://vk.com/alsldla"},
    ),
)
def test_logs_handler_wrong_input(params):
    path_handler = PathHandler(params)
    with pytest.raises(SystemExit):
        LogsHandler(path_handler).get_logs()
