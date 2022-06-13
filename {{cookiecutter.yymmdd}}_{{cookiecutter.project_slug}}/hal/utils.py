from pathlib import Path
from typing import Any

import numpy as np


def longpath(pth: Path) -> Path:
    """Converts input `pth` to long path compatible format"""
    return Path(r"//?/" + str(pth))


def clean_dict(d: dict) -> Any:
    """cleans up dictionary `d` for exporting as yaml
    dictionary is modified in-place (!)

    # https://stackoverflow.com/questions/59605943/python-convert-types-in-deeply-nested-dictionary-or-array

    """
    if isinstance(d, np.floating):
        return float(d)

    if isinstance(d, np.integer):
        return int(d)

    if isinstance(d, np.ndarray):
        return d.tolist()

    if isinstance(d, dict):
        for k, v in d.items():
            d.update({k: clean_dict(v)})

    return d
