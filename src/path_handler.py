from typing import Dict

from src.enums import PathTypes
from src.wrong_input_error import WrongPathError


class PathHandler:
    """Определяем тип пути и сам путь."""

    def __init__(self, mapped_params: Dict[str, str]):
        self.file_path = mapped_params.get("path", None)
        self.mapped_params = mapped_params
        self.path_type: str | None = None

    def is_available(self) -> bool:
        """Проверяем есть ли параметр format."""
        if self.file_path is None:
            return False
        return True

    def define_path_type(self) -> None:
        """Определяем тип пути к логам."""
        if self.is_available():
            if self.file_path[:8] == "https://":
                self.path_type = PathTypes.url.value
            else:
                self.path_type = PathTypes.local.value
        else:
            raise WrongPathError()