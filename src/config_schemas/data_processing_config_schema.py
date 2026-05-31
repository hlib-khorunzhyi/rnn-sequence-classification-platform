from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass

from config_schemas.data_processing import dataset_readers_schema


@dataclass
class DataProcessingConfig:
    version: str = MISSING
    data_local_save_dir: str = "./data/raw"
    dvc_remote_repo: str = (
        "https://github.com/hlib-khorunzhyi/rnn-sequence-classification-platform.git"
    )
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "hlib-khorunzhyi"
    github_access_token_secret_id: str = (
        "rnn-sequence-classification-platform-github-access-token"
    )

    dataset_reader_manager: dataset_readers_schema.DatasetReaderManagerConfig = MISSING


def setup_config() -> None:
    dataset_readers_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="data_processing_config_schema", node=DataProcessingConfig)
