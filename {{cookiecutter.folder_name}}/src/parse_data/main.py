import ultraplot as uplt
import random
import polars as pl
from hal.io import Output, save_fig, save_yaml
from hal.config import cfg
from hal.repro import reproduce


# %%
# additional / editable packages to log versions of
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
