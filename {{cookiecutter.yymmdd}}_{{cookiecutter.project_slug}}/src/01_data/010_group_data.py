# %%
from hal.config import cfg
from hal.repro import reproduce
from pathlib import Path

import numpy as np
import pandas as pd

# %%


# List additional dependencies to log
packages = [
    "numpy",
]

OUTPUT_PATH = reproduce(globals(), packages=packages)


# %%
# Global variables
