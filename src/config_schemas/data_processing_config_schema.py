from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass

from src.config_schemas.data_processing import (
    dataset_cleaner_schema,
    dataset_reader_schema,
)
from src.config_schemas.data_processing.dask_cluster import dask_cluster_schema


@dataclass
class DataProcessingConfig:
    version: str = MISSING
    data_local_save_dir: str = "./data/raw"
    dvc_remote_repo: str = (
        "https://github.com/hlib-khorunzhyi/rnn-sequence-classification-platform.git"
    )
    dvc_data_folder: str = "data/raw"
    github_user_name: str = "hlib-khorunzhyi"
    github_access_token_secret_id: str = "rnn-scp-data-access"

    dataset_reader_manager: dataset_reader_schema.DatasetReaderManagerConfig = MISSING
    dataset_cleaner_manager: dataset_cleaner_schema.DatasetCleanerManagerConfig = (
        MISSING
    )

    dask_cluster: dask_cluster_schema.DaskClusterConfig = MISSING

    processed_data_save_dir: str = MISSING

    run_tag: str = "default_run"

    docker_image_name: str = "rnn-sequence-classification-platform"
    docker_image_tag: str = "latest"

    min_nrof_words: int = 2


def setup_config() -> None:
    dataset_reader_schema.setup_config()
    dataset_cleaner_schema.setup_config()
    dask_cluster_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="data_processing_config_schema", node=DataProcessingConfig)
