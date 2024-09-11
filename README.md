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
├── README.md          <- The top-level README for developers using this project.
│
├── ava                <- Source code for use in this project.
│   ├── __init__.py    <- Makes a Python module
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
├── data               <- Raw input data.
│
├── hal                <- Folder with general use (global) scripts.
|
├── output             <- Files required for recreating the environment, eg
│
├── env                <- Files required for recreating the environment, eg
│                         generated with `pip freeze > requirements.txt`
│
├── pyproject.toml           <- makes project pip installable (pip install -e .) so src can be imported



```
