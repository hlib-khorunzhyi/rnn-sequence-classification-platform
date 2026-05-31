from hydra.utils import instantiate

from config_schemas.config_schema import Config
from utils.config_utils import get_config
from utils.data_utils import get_raw_data_with_version
from utils.gcp_utils import access_secret_version


@get_config(config_path="../configs", config_name="config")
def process_data(config: Config) -> None:
    # from omegaconf import OmegaConf
    # print(OmegaConf.to_yaml(config))
    # return

    github_access_token = access_secret_version(
        config.infrastructure.project_id,
        config.process_data.github_access_token_secret_id,
    )

    get_raw_data_with_version(
        version=config.process_data.version,
        data_local_save_dir=config.process_data.data_local_save_dir,
        dvc_remote_repo=config.process_data.dvc_remote_repo,
        dvc_data_folder=config.process_data.dvc_data_folder,
        github_username=config.process_data.github_user_name,
        github_access_token=github_access_token,
    )

    dataset_reader_manager = instantiate(config.process_data.dataset_reader_manager)
    df = dataset_reader_manager.read_data()

    print(df.head())
    print(df.tail())

    print(df.compute()["dataset_name"].unique())


if __name__ == "__main__":
    process_data()  # type: ignore
