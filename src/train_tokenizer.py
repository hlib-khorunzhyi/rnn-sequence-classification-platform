import os
from pathlib import Path

import pandas as pd
from hydra.utils import instantiate

from config_schemas.config_schema import Config
from utils import get_logger
from utils.config_utils import get_pickle_config
from utils.io_utils import write_yaml_file


@get_pickle_config(
    config_path="src/configs/automatically_generated", config_name="config"
)
def train_tokenizer(config: Config) -> None:
    logger = get_logger(Path(__file__).name)

    data_parquet_path = config.train_tokenizer.data_parquet_path
    text_column_name = config.train_tokenizer.text_column_name

    tokenizer = instantiate(config.train_tokenizer.tokenization, _convert_="all")

    logger.info("Reading dataset...")
    df = pd.read_parquet(data_parquet_path)

    logger.info("Starting training tokenizer...")
    tokenizer.train(df[text_column_name].values)

    logger.info("Saving trained tokenizer...")
    tokenizer_save_path = os.path.join(
        os.path.dirname(data_parquet_path), "trained_tokenizer"
    )
    tokenizer.save(tokenizer_save_path)

    docker_info = {
        "docker_image": config.train_tokenizer.docker_image_name,
        "docker_tag": config.train_tokenizer.docker_image_tag,
    }
    docker_info_save_path = os.path.join(tokenizer_save_path, "docker_info.yaml")

    write_yaml_file(docker_info_save_path, docker_info)

    logger.info("Done!")


if __name__ == "__main__":
    train_tokenizer()
