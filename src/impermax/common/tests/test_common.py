import logging
from unittest import TestCase

from src.impermax.common.path_consts import BASE_PATH

logger = logging.getLogger(__name__)


class TestCommonDir(TestCase):

    def test_base_path_points_to_base_impermax_dir(self):
        self.assertEqual(BASE_PATH.name, 'impermax')
