import numpy as np
import pandas as pd
import proplot as pplt
import yaml
from hal.config import cfg
from hal.fileIO import csv_to_dataframe
from hal.repro import reproduce
from hal.fmt import load_pplt_config
from pathlib import Path

# %%

load_pplt_config("paper")

# List additional dependencies to watermark
packages = [
    "numpy",
]

OUTPUT_PATH = cfg.paths.output / Path(__file__).stem
FIGURE_OUTPUT_PATH = cfg.paths.figures / Path(__file__).stem
OUTPUT_PATH = reproduce(globals(), packages=packages)
