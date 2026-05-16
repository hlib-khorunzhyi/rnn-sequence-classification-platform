from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class DVCConfig:
    dvc_remote_name: str = "gcs-storage"
    dvc_remote_url: str = "gs://u7501643495/data/raw"
    dvc_raw_data_folder: str = "data/raw"

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="dvc_config_schema", node=DVCConfig)