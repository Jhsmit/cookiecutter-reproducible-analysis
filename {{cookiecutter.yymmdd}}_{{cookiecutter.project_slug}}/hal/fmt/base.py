import proplot as pplt
from hal.config import cfg
from omegaconf import OmegaConf

CBAR_WIDTH = 5 / 25.4


pplt_cfg = OmegaConf.load(cfg.paths.root / "hal" / "fmt" / "proplot_presets.yaml")


def load_pplt_config(preset="paper"):
    dict_config = pplt_cfg[preset]
    primitive = OmegaConf.to_container(dict_config)
    pplt.rc.update(primitive)
