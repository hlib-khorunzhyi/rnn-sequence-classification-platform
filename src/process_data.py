import os
from pathlib import Path

import pandas as pd
from dask.distributed import Client
from hydra.utils import instantiate

from config_schemas.config_schema import Config
from data_processing.dataset_cleaners import DatasetCleanderManager
from utils import get_logger
from utils.config_utils import custom_instantiate, get_pickle_config
from utils.data_utils import (
    filter_based_on_minimum_number_of_words,
    get_raw_data_with_version,
)
from utils.gcp_utils import access_secret_version
from utils.io_utils import write_yaml_file


def process_raw_data(
    df_partition: pd.DataFrame, dataset_cleaner_manager: DatasetCleanderManager
) -> pd.Series:
    cleaned = df_partition["text"].apply(dataset_cleaner_manager)

    return cleaned.astype(str)


@get_pickle_config(config_path="src/configs/automatically_generated", config_name="config")  # type: ignore[untyped-decorator]
def process_data(config: Config) -> None:
    # from omegaconf import OmegaConf

    # print(OmegaConf.to_yaml(config))
    # return

    logger = get_logger(Path(__file__).name)
    logger.info("Processing raw data...")

    processed_data_save_dir = config.process_data.processed_data_save_dir

    cluster = custom_instantiate(config.process_data.dask_cluster)
    client = Client(cluster)

    try:
        # logger.info("started")
        # github_access_token = access_secret_version(
        #     config.infrastructure.project_id,
        #     config.process_data.github_access_token_secret_id,
        # )

        # logger.info("got github access token")
        # get_raw_data_with_version(
        #     version=config.process_data.version,
        #     data_local_save_dir=config.process_data.data_local_save_dir,
        #     dvc_remote_repo=config.process_data.dvc_remote_repo,
        #     dvc_data_folder=config.process_data.dvc_data_folder,
        #     github_username=config.process_data.github_user_name,
        #     github_access_token=github_access_token,
        # )
        # logger.info("got raw data with version")

        dataset_reader_manager = instantiate(config.process_data.dataset_reader_manager)
        dataset_cleaner_manager = instantiate(
            config.process_data.dataset_cleaner_manager
        )

        logger.info("instatiated dataset reader and cleaner managers")
        df = dataset_reader_manager.read_data()

        print(f"{df.npartitions=}")

        logger.info("Cleaning data...")
        df = df.assign(
            cleaned_text=df.map_partitions(
                process_raw_data,
                dataset_cleaner_manager=dataset_cleaner_manager,
                meta=("text", "str"),
            )
        )

        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        train_df = df[df["split"] == "train"]
        dev_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        train_df = filter_based_on_minimum_number_of_words(
            train_df, min_nrof_words=config.process_data.min_nrof_words
        )
        dev_df = filter_based_on_minimum_number_of_words(
            dev_df, min_nrof_words=config.process_data.min_nrof_words
        )
        test_df = filter_based_on_minimum_number_of_words(
            test_df, min_nrof_words=config.process_data.min_nrof_words
        )

        logger.info("Saving split data directly to Parquet via Dask...")

        train_df.to_parquet(train_parquet_path, write_index=False)
        dev_df.to_parquet(dev_parquet_path, write_index=False)
        test_df.to_parquet(test_parquet_path, write_index=False)

        docker_info = {
            "docker_image": config.process_data.docker_image_name,
            "docker_tag": config.process_data.docker_image_tag,
        }
        docker_info_save_path = os.path.join(
            processed_data_save_dir, "docker_info.yaml"
        )
        write_yaml_file(docker_info_save_path, docker_info)

        logger.info("Data precessing finished")

    finally:
        logger.info("Clossing dask client and cluster...")
        client.close()
        cluster.close()


if __name__ == "__main__":
    process_data()
