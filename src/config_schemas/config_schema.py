from dataclasses import field

from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass

from config_schemas import data_processing_config_schema, dvc_config_schema
from config_schemas.infrastructure import gcp_schema


@dataclass
class Config:
    version_data: dvc_config_schema.DVCConfig = field(
        default_factory=dvc_config_schema.DVCConfig
    )
    process_data: data_processing_config_schema.DataProcessingConfig = field(
        default_factory=data_processing_config_schema.DataProcessingConfig
    )
    infrastructure: gcp_schema.GCPConfig = field(default_factory=gcp_schema.GCPConfig)


def setup_config() -> None:
    dvc_config_schema.setup_config()
    data_processing_config_schema.setup_config()
    gcp_schema.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
