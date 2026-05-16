from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass

from omegaconf import MISSING


@dataclass
class DataProcessingConfig:
    version: str = MISSING
    data_local_save_dir: str = "./data/raw"
    dvc_remote_repo: str = "https://github.com/hlib-khorunzhyi/rnn-sequence-classification-platform.git"
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "hlib-khorunzhyi"
    github_access_token_secret_id: str = "rnn-sequence-classification-platform-github-access-token"

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="data_processing_config_schema", node=DataProcessingConfig)