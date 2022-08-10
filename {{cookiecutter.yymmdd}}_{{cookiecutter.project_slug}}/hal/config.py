from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from omegaconf import OmegaConf


@dataclass
class Paths(object):
    root: Path
    """Absolute path of the root directory"""

    output: Path
    """Absolute path of the output directory"""

    src: Path
    """Absolute path of the src directory"""

    report: Path
    """Absolute path of the report directory"""

    figures: Path
    """Absolute path of figure output directory"""

    data: Path
    """Absolute path of figure output directory"""

@dataclass
class TopLevelConf(object):
    paths: Paths


root = Path(__file__).parent.parent.absolute()

PATHS = Paths(
    root=root,
    output=root / "output",
    src=root / "src",
    report=root / "report",
    figures=root / "report" / "figures",
    data=root / "data"
)

toplevel = TopLevelConf(paths=PATHS)

root_cfg = OmegaConf.load(PATHS.root / "config.yaml")

# Convert entries in `paths` section to pathlib.Path objects
for k, v in root_cfg["paths"].items():
    root_cfg["paths"][k] = Path(v)
path_cfg = OmegaConf.structured(toplevel)

cfg = OmegaConf.merge(root_cfg, path_cfg)
