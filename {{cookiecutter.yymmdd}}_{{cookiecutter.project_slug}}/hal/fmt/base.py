import proplot as pplt
import yaml

from hal.config import cfg

pplt_cfg = yaml.safe_load(
    (cfg.root / "hal" / "fmt" / "proplot_presets.yaml").read_text()
)


def load_pplt_config(preset: str = "paper") -> None:
    dict_config = pplt_cfg[preset]
    pplt.rc.update(dict_config)
