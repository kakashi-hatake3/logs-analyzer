from sys import argv
from typing import List, Dict

from src.enums import InputParameters
from src.wrong_input_error import (
    WrongInputError,
    WrongParameterNameError,
    WrongCountParametersError,
)


class InputHandler:
    """Класс обрабатывающий входные данные."""

    @property
    def values(self) -> List[str]:
        return argv


class InputMapper:
    """Класс, который сопоставляет параметру его тело и в случае ошибки вызывает ее."""

    def __init__(self):
        self.parameters = InputHandler().values
        self.command_count = 0
        self._mapped_params: Dict[str, str] = {}

    def _map_input(self) -> None:
        """Заполняем словарь."""
        define_command_parameter_str = "--"
        is_should_add = False
        should_add_param = ""
        for parameter in self.parameters:
            if is_should_add:
                self._mapped_params[should_add_param] = parameter
                is_should_add = False
            if parameter[:2] == define_command_parameter_str:
                self.command_count += 1
                is_should_add = True
                should_add_param = parameter[2:]

    def get_mapped_params(self) -> Dict[str, str]:
        """Возвращаем словарь или печатает ошибку."""
        try:
            self._map_input()
            CheckParameters(
                self.parameters, self.command_count, self._mapped_params
            ).check_correctness()
        except WrongCountParametersError as e:
            print(e)
            exit()
        except WrongInputError as e:
            print(e)
            exit()
        except WrongParameterNameError as e:
            print(e)
            exit()
        else:
            return self._mapped_params


class CheckParameters:
    """Проверка параметров."""

    def __init__(self, parameters, command_count, mapped_params):
        self.mapped_params = mapped_params
        self.command_count = command_count
        self.parameters = parameters

    def check_correctness(self) -> None:
        """Проверяем на ошибку."""
        if len(self.parameters) < 3:
            raise WrongCountParametersError(len(self.parameters))
        if self.command_count * 2 + 1 != len(self.parameters):
            raise WrongInputError
        for key in self.mapped_params.keys():
            if key not in [
                InputParameters.path,
                InputParameters.from_date,
                InputParameters.to_date,
                InputParameters.file_format,
                InputParameters.filter_field,
                InputParameters.filter_value,
            ]:
                raise WrongParameterNameError(key)
