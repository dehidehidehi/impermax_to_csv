from abc import ABC, abstractmethod

from src.impermax.common.path_consts import TARGET_CSV


class DaoInterface(ABC):

    @staticmethod
    def _create_output_dir() -> None:
        TARGET_CSV.mkdir(exist_ok=True, parents=True)

    @abstractmethod
    def save(self) -> None:
        """"""