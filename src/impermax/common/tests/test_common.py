import logging
from unittest import TestCase

from src.impermax.common.path_consts import BASE_PATH

logger = logging.getLogger(__name__)


class TestCommonDir(TestCase):
    def test_base_path_points_to_base_impermax_dir(self):
        """Some CI/CD pipelines (GitHub actions) will rename the base dir name to the repo name."""
        self.assertIn(BASE_PATH.name, ("impermax", "impermax_to_csv"))
