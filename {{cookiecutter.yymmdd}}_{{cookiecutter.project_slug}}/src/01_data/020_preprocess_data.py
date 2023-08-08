# %%
from hal.repro import reproduce

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

NUM = 20
OVERWRITE = True
rng = np.random.RandomState()

# %%

col_names = [f"col_{c}" for c in range(NUM)]
data = rng.rand(30, NUM)
df = pd.DataFrame(data, columns=col_names)
