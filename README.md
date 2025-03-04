# cookiecutter-reproducible-analysis

Cookiecutter for creating a project structure facilitating reproducible analysis.



## The resulting directory structure

The directory structure of your new project looks like this: 

```

├── LICENSE
├── README.md                   <- The top-level README for developers using this project.
│           
├── ava                         <- Source code for use in this project.
│   ├── __init__.py             <- Makes a Python module
|   |           
|   ├── prod                    <- Folder with 'final' production scripts
│   │   └── script_x            <- folder containing one script / analysis module
│   │      ├── output           <- output folder for this module
│   │      │    └── _rpr.zip    <- reproducibility archive
│   │      └── main.py          <- script / analysis module
│   │           
│   ├── stage                   <- Staging area.
│   │           
│   ├── toolbox                 <- General use classes/functions/constants.
│           
├── data                        <- Raw input data (small files only).
│           
├── editable                    <- Folder with editable installed libraries.    
│           
├── hal                         <- Folder with general use (global) scripts.
│           
├── metadata                    <- Metadata for the project
|           
├── config.yaml                 <- config settings available in hal.config.cfg object    
├── freeze.txt                  <- Output of pip freeze from the most recently ran script.    
├── pyproject.toml              <- makes project pip installable (pip install -e .) so ava can be imported


```

## Usage

Install `cookiecutter`, then run: 

    cookiecutter gh:jhsmit/cookiecutter-reproducible-analysis

CD into the newly created directory, then create and activate your venv. 

Install the project:

    uv pip install -e .


Checkout any libraries you want to use in editable mode, eg

    git checkout https://github.com/Jhsmit/dont-fret.git editable/dont-fret

Install any editable library:

    uv pip install -e editable/dont-fret


Create/copy a folder in the 'stage' directory, when you are happy with the script, move it to the 'prod' folder. 

## Reproducibility

Each folder has a script (`main.py`) which generates some output in the corresponding `output` folder. To make scripts reproducible, use the following code snippet:

```python

from hal.repro import reproduce

packages = ["numpy", "dont_fret", "smitfit"]
OUTPUT_PATH = reproduce(globals(), packages=packages)

```

The `reproduce` function will create a zip file in the `output` folder with the name `_rpr.zip`. This zip file contains the script, the current toolbox, and the versions of the packages used. The returned constant `OUTPUT_PATH` is the path to the output folder.


## Output

For managing script output you can use the `Output` class. Consider the following example:

```python

import ultraplot as uplt
import random
import polars as pl
from hal.io import Output, save_fig, save_yaml
from hal.config import cfg
from hal.repro import reproduce

packages = ["numpy", "dont_fret", "smitfit"]
OUTPUT_PATH = reproduce(globals(), packages=packages)
OVERWRITE = False  # set to True to overwrite existing files


def do_fit(data):
    return {"a": random.random(), "b": random.random()}


def make_plot(data):
    fig, ax = uplt.subplots(aspect=1.618)
    ax.scatter(data["x"], data["y"])
    return fig


input_files = cfg.paths["external_data"]

for csv_file in input_files.glob("*.csv"):
    output = Output(
        OUTPUT_PATH / csv_file.stem, overwrite=OVERWRITE, files=["fit.yaml", "plot.png"]
    )

    if output.skip:
        continue

    data = pl.read_csv(csv_file)
    fit = do_fit(data)
    fig = make_plot(data)

    save_yaml(fit, output["fit.yaml"])
    save_fig(fig, output["plot.png"])
    uplt.close(fig)

    assert output.done

```

Aside from creating a output folder with the reprodicibility .zip file, we are also using the `Output` class to keep track of the scripts' expected output. If the `OVERWRITE` flag is set to `True`, `output.skip` always returns false thus each file in the for loop is processed. Otherwise, `output.skip` return `True` only if both expected output files exists. This is very useful for a scenario where more data is added to the 'external_data' folder such that the script only processes new data. On the other hand, if the script is updated the overwrite flag can be set to `True` to reprocess all data. Finally, the `output.done` flag is set to `True` if all expected output files are created. This is useful for checking if the script has finished processing all data.

### Credits

This cookiecutter is inspired by / derived from:

https://github.com/drivendata/cookiecutter-data-science
https://github.com/mkrapp/cookiecutter-reproducible-science
https://github.com/timtroendle/cookiecutter-reproducible-research
