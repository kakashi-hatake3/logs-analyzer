from typing import Dict

from src.enums import Formats, InputParameters
from src.wrong_input_error import WrongParameterNameError


class FormatHandler:
    """Обрабатываем format."""

    def __init__(self, mapped_params: Dict[str, str]):
        self.file_format = mapped_params.get(InputParameters.file_format, None)
        self.formats = (Formats.adoc.value, Formats.markdown.value)

    def get_format(self) -> str | None:
        """Возвращаем проверенный формат, None или ошибку.

        :return: str | None | WrongParameterNameError
        """
        check_format = CheckFormatCorrectness(self.file_format)
        if check_format.is_none_check():
            try:
                check_format.checking_written_correctly(self.formats)
            except WrongParameterNameError as e:
                return e
            else:
                return self.file_format


class CheckFormatCorrectness:

    def __init__(self, file_format):
        self.file_format = file_format

    def is_none_check(self) -> bool:
        """Проверяем есть ли параметр format."""
        if self.file_format is None:
            return False
        return True

    def checking_written_correctly(self, formats) -> None:
        """Проверяем правильность написания формата."""
        if self.file_format not in formats:
            raise WrongParameterNameError(self.file_format)
