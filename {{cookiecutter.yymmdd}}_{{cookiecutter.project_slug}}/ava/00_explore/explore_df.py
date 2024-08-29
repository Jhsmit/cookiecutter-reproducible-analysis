# %%
import numpy as np
import polars as pl

from hal.components import ScatterPlot

# create a sample Polars DataFrame
np.random.seed(0)
df = pl.DataFrame(
    {
        "x": np.arange(100) * np.random.rand(100),
        "y": np.cumsum(np.random.rand(100)),
        "category": np.random.choice(["A", "B", "C"], 100),
        "size": np.random.rand(100) * 10,
        "color": np.random.choice(["red", "green", "blue"], 100),
    }
)


ScatterPlot(df)
# %%
