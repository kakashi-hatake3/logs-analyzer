from typing import Dict

from src.enums import Formats
from src.wrong_input_error import WrongParameterNameError


class FormatHandler:
    """Обрабатываем format."""

    def __init__(self, mapped_params: Dict[str, str]):
        self.file_format = mapped_params.get("format", None)
        self.formats = (Formats.adoc.value, Formats.markdown.value)

    def is_available(self) -> bool:
        """Проверяем есть ли параметр format."""
        if self.file_format is None:
            return False
        return True

    def _check_correctness(self) -> None:
        """Проверяем правильность написания формата."""
        if self.file_format not in self.formats:
            raise WrongParameterNameError(self.file_format)

    def get_format(self) -> str | Exception:
        """Возвращаем проверенный формат."""
        if self.is_available():
            try:
                self._check_correctness()
            except WrongParameterNameError as e:
                return e
            else:
                return self.file_format
