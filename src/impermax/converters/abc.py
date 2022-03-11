from abc import ABC, abstractmethod

from src.impermax.common.consts import TARGET_CSV


class ImpermaxOutputABC(ABC):

    @staticmethod
    def _create_output_dir() -> None:
        TARGET_CSV.mkdir(exist_ok=True, parents=True)

    @abstractmethod
    def save(self) -> None:
        """"""