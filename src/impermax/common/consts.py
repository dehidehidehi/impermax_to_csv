from pathlib import Path

_common = Path(__file__).parent
_impermax = _common.parent
_src = _impermax.parent

BASE_PATH = _src.parent
TARGET_CSV = BASE_PATH / 'target' / 'csv'