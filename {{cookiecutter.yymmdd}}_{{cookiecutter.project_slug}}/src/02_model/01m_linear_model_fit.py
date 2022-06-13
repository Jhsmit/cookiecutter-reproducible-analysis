# %%


import numpy as np
import pandas as pd
import proplot as pplt
import yaml
from hal.config import cfg
from hal.fileIO import csv_to_dataframe
from hal.repro import reproduce

# %%

load_pplt_config("paper")

# List additional dependencies to log
packages = [
    "numpy",
]

OUTPUT_PATH = cfg.paths.output / Path(__file__).stem
FIGURE_OUTPUT_PATH = cfg.paths.figures / Path(__file__).stem
reproduce(OUTPUT_PATH, globals(), packages=packages)
