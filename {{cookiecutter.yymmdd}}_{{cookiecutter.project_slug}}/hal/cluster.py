import warnings

from dask.distributed import LocalCluster, Worker
from hal.config import cfg
import time
from omegaconf.dictconfig import DictConfig
from omegaconf import OmegaConf

kwargs = {"threads_per_worker": 1, "memory_limit": "25GB"}


def blocking_cluster(config: DictConfig):
    """Start a dask LocalCluster and block until interrupted"""

    cfg_dic = OmegaConf.to_container(config)
    address = cfg_dic.pop("address")
    ip, port = int(address.split(":"))
    if ip not in ["127.0.0.1", "localhost"]:
        warnings.warn("Starting local cluster but specified IP is not local")
    local_cluster = LocalCluster(scheduler_port=port, **cfg_dic)
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
