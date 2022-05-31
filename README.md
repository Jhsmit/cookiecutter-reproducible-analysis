# cookiecutter-reproducible-analysis
Cookiecutter for creating a project structure facilitating reproducible analysis 


### The resulting directory structure

The directory structure of your new project looks like this: 

├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default MkDocs project
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── environment        <- Files required for recreating the environment, eg
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── 01_data        <- Downloading or preprocessing of data
│   │
│   ├── 02_model       <- Scripts to turn raw data into features for modeling
│   │
│   └── 03_view        <- Scripts to create exploratory and results oriented visualizations
│       
│
└── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io