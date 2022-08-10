from functools import reduce
from pathlib import Path
from typing import Any, Optional
from collections import OrderedDict

import numpy as np


def longpath(pth: Path) -> Path:
    """Converts input `pth` to long attr compatible format"""
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

# https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties/31174427#31174427
def rsetattr(obj: Any, attr: str, val: Any) -> Any:
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

# https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-subobjects-chained-properties/31174427#31174427
def rgetattr(obj: Any, attr: str, *default):
    try:
        return reduce(getattr, attr.split('.'), obj)
    except AttributeError as e:
        if default:
            return default[0]
        else:
            raise e

def rhasattr(obj: Any, attr:str):
    try:
        reduce(getattr, attr.split("."), obj)
        return True
    except AttributeError:
        return False

