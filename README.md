# cookiecutter-reproducible-analysis

Cookiecutter for creating a project structure facilitating reproducible analysis.



## The resulting directory structure

The directory structure of your new project (after installation) looks like this: 

```

├── LICENSE
├── README.md                   <- The top-level README for developers using this project.
│           
├── src                         <- Source code for use in this project.
│   ├── __init__.py             <- Makes a Python module
|   |           
|   └── parse_data              <- Folder a set of related scripts / analysis modules.
│      ├── output              <- output folder for this module
│      │    └── _rpr.zip       <- reproducibility archive
│      └── main.py             <- folder containing one script / analysis module

├── data                        <- Raw input data (small files only).
│           
├── editable                    <- Folder with editable installed libraries.    
│           
├── ava                         <- Folder with general use (global) scripts.
│           
├── metadata                    <- Metadata for the project
|           
├── config.yaml                 <- config settings available in hal.config.cfg object    
├── uv.lock                     <- lockfile created and used by uv to create reproducible environments
├── pyproject.toml              <- defines the project and sources for uv to create a uv.lock file


```

## Usage

Install `cookiecutter`, then run: 

```bash
$ cookiecutter gh:jhsmit/cookiecutter-reproducible-analysis
```

CD into the newly created directory and then:

Install the project:

```bash
$ uv sync
```

This will download and install the [HAL](https://github.com/Jhsmit/hal) general utility and reproducibility library from GitHub as well as the other basic dependencies. 

Initiate git:

```bash
$ git init
```

You can add a remote repository if you want or the project as a local git repository. In either case, make sure to back up your work regularly!

> [!CAUTION]
> Ideally, scripts should be backed up on a remote git repository, and script output should be backed up on a cloud storage solution or institutional storage. I haven't yet found a good solution which automatically backs up script output while ignoring the .venv folder. If you have any suggestions, please open an issue on GitHub.

### Adding dependencies

To keep the output reproducible, dependencies are managed via `uv` to ensure they are recorded in the lockfile. 

To add a new dependency from PyPI:

```bash
$ uv add package_name
```

To add a new dependency from a git repository:

```bash
uv add git+https://github.com/OpenSMFS/FRETBursts --rev 929ff403a6731c9474740dd5514f48ddb72f4a6a
```

Make sure to include the exact commit sha in the `--rev` argument to ensure reproducibility.

For adding dependencies from other sources see the UV docs on [dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-sources). 


### Using the editable folder. 


The `editable` folder is intended to contain libraries you are actively developing while working on this project. To add a library to this folder, first clone it there, and then install via uv. 

For example, to add the `dont-fret` library:

```bash
$ git clone https://github.com/Jhsmit/dont-fret.git editable/dont-fret
```


Then to install:

```bash
uv add ./editable/dont-fret
```

The reproducibility script from the `hal` library will then also record the version of the currently checked out code in the `dont-fret` library when running scripts.

> [!NOTE]
> that it is recommended to only use editable libraries in development and rather use fixed version from PyPI or git repos for production / final analyses.


## Reproducibility

Each folder has one or more scripts which generate some output in the corresponding `output` folder. To make scripts reproducible, use the following code snippet:

```python

from hal.repro import reproduce

packages = ["numpy", "dont_fret", "smitfit"]
OUTPUT_PATH = reproduce(globals(), packages=packages)

```

The `reproduce` function will create a zip file in the `output` folder with the name `_rpr.zip`. This zip file contains the script, the current `ava`, and the versions of the packages used. The returned constant `OUTPUT_PATH` is the path to the output folder.


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
