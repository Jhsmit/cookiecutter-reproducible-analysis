
from hal.repro import reproduce


# %%

# additional / editable packages to log versions pf
packages = ["numpy", "matplotlib"]
OUTPUT_PATH = reproduce(globals(), packages=packages)
