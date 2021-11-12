from abc import ABC, abstractmethod

from impermax.common.consts import OUTPUT_PATH


class ImpermaxOutputABC(ABC):

    @staticmethod
    def _create_output_dir() -> None:
        OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

    @abstractmethod
    def save(self) -> None:
        """"""