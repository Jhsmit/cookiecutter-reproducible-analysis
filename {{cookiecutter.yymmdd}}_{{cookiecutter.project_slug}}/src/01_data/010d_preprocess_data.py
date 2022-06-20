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

NUM = 20
OVERWRITE = True
rng = np.random.RandomState()

#%%

col_names = [f"col_{c}" for c in range(NUM)]
data = rng.rand(30, NUM)
df = pd.DataFrame(data, columns=col_names)

dataframe_to_file(df, OUTPUT_PATH / "gen_data.csv", fmt="csv")
