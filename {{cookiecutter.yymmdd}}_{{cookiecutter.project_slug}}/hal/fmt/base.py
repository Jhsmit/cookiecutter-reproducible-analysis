from omegaconf import OmegaConf
import proplot as pplt

CBAR_WIDTH = 5 / 25.4


pplt_cfg = OmegaConf.load("proplot_presets.yaml")


def load_pplt_config(preset="paper"):
    dict_config = pplt_cfg[preset]
    primitive = OmegaConf.to_container(dict_config)
    pplt.rc.update(primitive)
