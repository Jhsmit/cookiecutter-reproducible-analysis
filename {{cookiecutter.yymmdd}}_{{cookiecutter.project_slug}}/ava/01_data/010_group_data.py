# %%
from pathlib import Path

from hal.config import cfg
from hal.repro import reproduce

# %%


# List additional dependencies to log
packages = [
    "numpy",
]

OUTPUT_PATH = reproduce(globals(), packages=packages)


# %%
# Global variables
