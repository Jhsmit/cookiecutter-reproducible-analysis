import warnings
from typing import Union, Optional

from dask.distributed import LocalCluster, Client
from hal.config import cfg
import time
from omegaconf.dictconfig import DictConfig
from omegaconf import OmegaConf


def get_client(cluster_name: Optional[str] = None) -> Union[Client, None]:
    """Attempts to connect to a Dask cluster and returns the Client

    """
    client = None
    if cluster_name is None:
        for cluster_name in cfg.clusters:
            try:
                client = Client(cfg.clusters[cluster_name].address, timeout=1)
            except OSError:
                continue
    else:
        client = Client(cfg.clusters[cluster_name].address, timeout=5)

    return client


def blocking_cluster(config: Union[dict, DictConfig]) -> None:
    """Start a dask LocalCluster and block until interrupted"""

    if isinstance(config, DictConfig):
        cfg_dic = OmegaConf.to_container(config)
    else:
        cfg_dic = config

    address = cfg_dic.pop("address")
    ip, port = address.split(":")
    if ip not in ["127.0.0.1", "localhost"]:
        warnings.warn("Starting local cluster but specified IP is not local")
    local_cluster = LocalCluster(scheduler_port=int(port), **cfg_dic)
    try:
        loop = True
        while loop:
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                print("Interrupted")
                loop = False
    finally:
        local_cluster.close()


if __name__ == "__main__":
    blocking_cluster(cfg["cluster"])
