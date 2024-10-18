from sys import argv
from typing import List, Dict

from src.wrong_input_error import WrongCountParametersError
from src.wrong_input_error import WrongInputError, WrongParameterNameError


class InputHandler:
    """Класс обрабатывающий входные данные."""

    @property
    def values(self) -> List[str]:
        return argv


class InputMapper:
    """Класс, который сопоставляет параметру его тело и в случае ошибки вызывает ее."""

    def __init__(self):
        self.parameters = InputHandler().values
        self._command_count = 0
        self._mapped_params: Dict[str, str] = {}

    def _map_input(self) -> None:
        """Заполняем словарь."""
        is_should_add = False
        should_add_param = ""
        for parameter in self.parameters:
            if is_should_add:
                self._mapped_params[should_add_param] = parameter
                is_should_add = False
            if parameter[:2] == "--":
                self._command_count += 1
                is_should_add = True
                should_add_param = parameter[2:]

    def _check_is_correct(self) -> None:
        """Проверяем на ошибку."""
        if len(self.parameters) < 3:
            raise WrongCountParametersError(len(self.parameters))
        if self._command_count * 2 + 1 != len(self.parameters):
            raise WrongInputError
        for key in self._mapped_params.keys():
            if key not in ["path", "from", "to", "format", "filter-field", "filter-value"]:
                raise WrongParameterNameError(key)

    def get_mapped_params(self) -> Dict[str, str] | Exception:
        """Возвращаем словарь или ошибку."""
        try:
            self._map_input()
            self._check_is_correct()
        except WrongCountParametersError as e:
            return e
        except WrongInputError as e:
            return e
        except WrongParameterNameError as e:
            return e
        else:
            return self._mapped_params
