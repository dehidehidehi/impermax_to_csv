"""
|  Tests are located in each layer and component of the application.
|  This convenience function serves the purpose of running tests from within a Python script.
|
|  Alternatively, run the following command at the root of this project:
|  `python -m unittest discover --start-directory ./src`
"""
from unittest import TestLoader, TextTestRunner

from src.impermax.common.path_consts import BASE_PATH


def discover_and_run_tests() -> None:
    loader = TestLoader()
    suite = loader.discover(BASE_PATH, pattern="test_*")
    test_runner = TextTestRunner(verbosity=1)
    test_runner.run(suite)


if __name__ == "__main__":
    discover_and_run_tests()
