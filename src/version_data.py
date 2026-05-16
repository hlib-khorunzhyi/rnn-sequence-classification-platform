from config_schemas.config_schema import Config
from utils.config_utils import get_config
from utils.data_utils import (
    initialize_dvc,
    initialize_dvc_storage,
    make_new_data_version,
)

@get_config(config_path="../configs", config_name="config")  # type: ignore[untyped-decorator]
def version_data(config: Config) -> None:
    initialize_dvc()

    initialize_dvc_storage(config.version_data.dvc_remote_name, config.version_data.dvc_remote_url)

    make_new_data_version(config.version_data.dvc_raw_data_folder, config.version_data.dvc_remote_name)


if __name__ == "__main__":
    version_data()
