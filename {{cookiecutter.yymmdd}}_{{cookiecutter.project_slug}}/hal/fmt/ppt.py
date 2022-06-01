from hal.fmt.base import *
import proplot as pplt

# TODO move to yaml / whatever files
settings = {
    "font.family": "Arial",
    "font.size": 25,
    "meta.width": 2,
    "tick.len": 10,
}

pplt.rc.update(settings)
