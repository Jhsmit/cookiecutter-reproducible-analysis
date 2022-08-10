#%%
# from hal.config import cfg
# from hal.repro import reproduce
from pathlib import Path

import numpy as np
import pandas as pd
from hal.fileIO import dataframe_to_file

#%%


# List additional dependencies to log
packages = [
    "numpy",
]

OUTPUT_PATH = cfg.paths.output / Path(__file__).stem
reproduce(OUTPUT_PATH, globals(), packages=packages)


#%%
# Global variables

