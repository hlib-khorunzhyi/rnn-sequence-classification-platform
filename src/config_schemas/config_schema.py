from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass
from dataclasses import field

from config_schemas.dvc_config_schema import DVCConfig
from config_schemas.infrastructure.gcp_schema import GCPConfig
from config_schemas.data_processing_config_schema import DataProcessingConfig


@dataclass
class Config:
    version_data: DVCConfig = field(default_factory=DVCConfig)
    process_data: DataProcessingConfig = field(default_factory=DataProcessingConfig)
    infastructure: GCPConfig = field(default_factory=GCPConfig)

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
