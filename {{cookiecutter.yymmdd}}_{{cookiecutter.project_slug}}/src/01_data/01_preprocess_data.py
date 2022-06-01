#%%
from hal.paths import PATHS
from hal.repro import reproduce
from hal.util import longpath
from typing import Union
from functools import partial
from pathlib import Path
import shutil
from dask.distributed import Client, progress
import numpy as np
from tools.process import process_ptu_file
import yaml

#%%


#%%

# List additional dependencies to log
packages = [
    "dont_fret",
]

OVERWRITE = False

z = 1
OUTPUT_PATH = longpath(PATHS.output / "bursts" / str(z).zfill(5))
SCRIPT_PATH = Path(__file__).absolute()
reproduce(SCRIPT_PATH, OUTPUT_PATH, globals(), packages=packages)

BS_KWARGS = {"T": 500e-6, "L": 50, "M": 35}


#%%

ptu_files = PATHS.input_path.glob("**/*.ptu")
ptu_files = [longpath(pth) for pth in ptu_files]

#%%

# single run:
# props = process_ptu_file(ptu_files[0], PATHS.input_path, OUTPUT_PATH, **BS_KWARGS)

client = Client("127.0.0.1:53254")

#%%


def is_done(ptu_file: Path, data_dir: Path, output_dir: Path) -> bool:
    """Checks if the ptu file is already processed"""

    rel_path = ptu_file.relative_to(data_dir)
    rel_path = Path(*[f.stem.replace(".sptw", "") for f in rel_path.parents][::-1])
    output_pth = output_dir / rel_path

    csv_output = output_pth / f"{ptu_file.stem}_DCBS.csv"
    return csv_output.exists()


#%%

func = partial(
    process_ptu_file,
    data_dir=longpath(PATHS.input_path),
    output_dir=OUTPUT_PATH,
    **BS_KWARGS,
)


if OVERWRITE:
    tasks = ptu_files
else:
    tasks = [
        ptu
        for ptu in ptu_files
        if not is_done(ptu, longpath(PATHS.input_path), OUTPUT_PATH)
    ]

futures = client.map(func, tasks)
progress(futures, notebook=False)
#
result = client.gather(futures)
#
print(result)
#
# TODO check for too long filenames!
#
# 'https://stackoverflow.com/questions/55815617/pathlib-path-rglob-fails-on-long-file-paths-in-windows'
# https: // stackoverflow.com / questions / 55815617 / pathlib - path - rglob - fails - on - long - file - paths - in -windows
