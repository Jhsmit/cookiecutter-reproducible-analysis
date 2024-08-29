# %%


import numpy as np
import pandas as pd
import proplot as pplt
import yaml
from hal.config import cfg
from hal.repro import reproduce
from hal.fmt import load_pplt_config

# %%

load_pplt_config("paper")

# List additional dependencies to log
packages = [
    "numpy",
]

OUTPUT_PATH = reproduce(globals(), packages=packages)
