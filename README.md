# cookiecutter-reproducible-analysis

**WORK IN PROGRESS REPOSITORY**

Cookiecutter for creating a project structure facilitating reproducible analysis 

This is a derivation of: 

https://github.com/drivendata/cookiecutter-data-science

https://github.com/mkrapp/cookiecutter-reproducible-science

https://github.com/timtroendle/cookiecutter-reproducible-research


### The resulting directory structure

The directory structure of your new project looks like this: 

```

├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
│
├── archive            <- Folder with scripts of previous versions.
│
├── hal                <- Folder with general use (global) scripts.
│
├── data               <- Raw input data.
│
├── docs               <- A default MkDocs project
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, Markdown, PDF, LaTeX, etc.
│
├── env                <- Files required for recreating the environment, eg
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
|   |
|   ├── 00_explore     <- Scripts/notebooks to (interactively) explore the data.
│   │
│   ├── 01_data        <- Downloading or preprocessing of data.
│   │
│   ├── 02_model       <- Scripts to create models or do modelling.
│   │
│   ├── 03_view        <- Scripts to create visualizations.
|   |
│   └── toolbox        <- general use scripts / functions specific to this project   
│
└── run_tasks          <- run scripts, start clusters, or code formatting

```

Note: when dask cluster has toolbox cached, changes made here are not directly propagated;
this might lead to irreproducible results