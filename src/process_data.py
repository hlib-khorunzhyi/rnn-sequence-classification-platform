from pathlib import Path
import os

import dask.dataframe as dd
import pandas as pd
from dask.distributed import Client
from hydra.utils import instantiate

from config_schemas.config_schema import Config
from data_processing.dataset_cleaners import DatasetCleanderManager
from utils import get_logger
from utils.config_utils import get_config, get_pickle_config, custom_instantiate
from utils.data_utils import get_raw_data_with_version
from utils.gcp_utils import access_secret_version


def process_raw_data(
    df_partition: pd.DataFrame,
    dataset_cleaner_manager: DatasetCleanderManager
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

        print(df.compute().head())
        exit(0)

        print(f"{df.npartitions=}")

        logger.info("Cleaning data...")
        df = df.assign(
            cleaned_text=df.map_partitions(
                process_raw_data, dataset_cleaner_manager=dataset_cleaner_manager,
                meta=("text", "str")
            )
        )

        train_parquet_path = os.path.join(processed_data_save_dir, "train.parquet")
        dev_parquet_path = os.path.join(processed_data_save_dir, "dev.parquet")
        test_parquet_path = os.path.join(processed_data_save_dir, "test.parquet")

        logger.info("Saving split data directly to Parquet via Dask...")

        # df[df["split"] == "train"].to_parquet(train_parquet_path, write_index=False)
        # df[df["split"] == "dev"].to_parquet(dev_parquet_path, write_index=False)
        # df[df["split"] == "test"].to_parquet(test_parquet_path, write_index=False)

        logger.info("Data precessing finished")

    finally:
        logger.info("Clossing dask client and cluster...")
        client.close()
        cluster.close()


if __name__ == "__main__":
    process_data()
