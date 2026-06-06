from hydra.utils import instantiate

from config_schemas.config_schema import Config
from utils.config_utils import get_config
from utils.data_utils import get_raw_data_with_version
from utils.gcp_utils import access_secret_version


@get_config(config_path="../configs", config_name="config")  # type: ignore[untyped-decorator]
def process_data(config: Config) -> None:
    from omegaconf import OmegaConf

    print(OmegaConf.to_yaml(config))
    return

    print("started")
    github_access_token = access_secret_version(
        config.infrastructure.project_id,
        config.process_data.github_access_token_secret_id,
    )

    print("got github access token")
    get_raw_data_with_version(
        version=config.process_data.version,
        data_local_save_dir=config.process_data.data_local_save_dir,
        dvc_remote_repo=config.process_data.dvc_remote_repo,
        dvc_data_folder=config.process_data.dvc_data_folder,
        github_username=config.process_data.github_user_name,
        github_access_token=github_access_token,
    )
    print("got raw data with version")

    dataset_reader_manager = instantiate(config.process_data.dataset_reader_manager)
    dataset_cleaner_manager = instantiate(config.process_data.dataset_cleaner_manager)

    print("instatiated")
    df = dataset_reader_manager.read_data().compute()
    print("computed")
    sample_df = df.sample(n=10)

    for _, row in sample_df.iterrows():
        text = row["text"]
        cleaned_text = dataset_cleaner_manager(text)

        print(60 * "*")
        print(f"{text=}")
        print(f"{cleaned_text=}")
        print(60 * "*")


if __name__ == "__main__":
    process_data()
