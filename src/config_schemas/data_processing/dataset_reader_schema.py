from typing import Optional

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic.dataclasses import dataclass


@dataclass
class DatasetReaderConfig:
    _target_: str = MISSING
    dataset_dir: str = MISSING
    dataset_name: str = MISSING
    gcp_project_id: str = SI("${infrastructure.project_id}")
    gcp_github_access_token_secret_id: str = SI(
        "${process_data.github_access_token_secret_id}"
    )
    dvc_remote_repo: str = SI("${process_data.dvc_remote_repo}")
    github_user_name: str = SI("${process_data.github_user_name}")
    version: str = SI("${process_data.version}")


@dataclass
class GHCDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = "src.data_processing.dataset_readers.GHCDatasetReader"
    dev_split_ratio: float = MISSING


@dataclass
class JigsawToxicCommentsDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = (
        "src.data_processing.dataset_readers.JigsawToxicCommentDatasetReader"
    )
    dev_split_ratio: float = MISSING


@dataclass
class TwitterDatasetReaderConfig(DatasetReaderConfig):
    _target_: str = "src.data_processing.dataset_readers.TwitterDatasetReader"
    dev_split_ratio: float = MISSING
    test_split_ratio: float = MISSING


@dataclass
class DatasetReaderManagerConfig:
    _target_: str = "src.data_processing.dataset_readers.DatasetReaderManager"
    dataset_readers: dict[str, DatasetReaderConfig] = MISSING
    repartition: bool = True
    target_partition_size: str = "10MB"
    available_memory: Optional[float] = None


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(
        name="dataset_reader_manager_schema",
        node=DatasetReaderManagerConfig,
        group="process_data/dataset_reader_manager",
    )
    cs.store(
        name="ghc_dataset_reader_schema",
        node=GHCDatasetReaderConfig,
        group="process_data/dataset_reader_manager/dataset_reader",
    )
    cs.store(
        name="jtc_dataset_reader_schema",
        node=JigsawToxicCommentsDatasetReaderConfig,
        group="process_data/dataset_reader_manager/dataset_reader",
    )
    cs.store(
        name="twitter_dataset_reader_schema",
        node=TwitterDatasetReaderConfig,
        group="process_data/dataset_reader_manager/dataset_reader",
    )
