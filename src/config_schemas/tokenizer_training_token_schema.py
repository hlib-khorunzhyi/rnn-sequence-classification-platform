from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass

import src.config_schemas.tokenization.tokenizer_schema as tokenizer_schemas


@dataclass
class TokenaizerTrainingConfig:
    docker_image_name: str = "rnn-sequence-classification-platform"
    docker_image_tag: str = "latest"

    # TODO: change the name to tokenizer
    tokenization: tokenizer_schemas.TokenizerConfig = MISSING

    data_parquet_path: str = MISSING
    text_column_name: str = MISSING


def setup_config() -> None:
    tokenizer_schemas.setup_config()

    cs = ConfigStore.instance()
    cs.store(name="tokenizer_training_config_schema", node=TokenaizerTrainingConfig)
