from pathlib import Path
from typing import Any
from collections import OrderedDict

import numpy as np


def longpath(pth: Path) -> Path:
    """Converts input `pth` to long path compatible format"""
    return Path(r"//?/" + str(pth))


def clean_types(d: Any) -> Any:
    """cleans up nested dict/list/tuple/other `d` for exporting as yaml

    Converts library specific types to python native types, including numpy dtypes,
    OrderedDict, numpy arrays
    
    # https://stackoverflow.com/questions/59605943/python-convert-types-in-deeply-nested-dictionary-or-array

    """
    if isinstance(d, np.floating):
        return float(d)

    if isinstance(d, np.integer):
        return int(d)

    if isinstance(d, np.ndarray):
        return d.tolist()

    if isinstance(d, list):
        return [clean_types(item) for item in d]

    if isinstance(d, tuple):
        return tuple(clean_types(item) for item in d)

    if isinstance(d, OrderedDict):
        return clean_types(dict(d))

    if isinstance(d, dict):
        return {k: clean_types(v) for k, v in d.items()}

    else:
        return d
