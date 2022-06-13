#%%

from hal.config import cfg
from hal.fmt import load_pplt_config
from hal.repro import reproduce

from pathlib import Path

#%%

# List additional dependencies to log
packages = [
    "dont_fret",
]


load_pplt_config()

OUTPUT_PATH = cfg.paths.figures / __file__.stem
OUTPUT_PATH.mkdir(exists_ok=True, parents=True)

SCRIPT_PATH = Path(__file__).absolute()
reproduce(SCRIPT_PATH, OUTPUT_PATH, globals(), packages=packages) #is __file__ in globals?
