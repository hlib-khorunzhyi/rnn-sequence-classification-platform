from pathlib import Path

from pytorch_end_to_end.config_schemas.config_schema import Config
from pytorch_end_to_end.utils.config_utils import get_config
from pytorch_end_to_end.utils.data_utils import initilaze_dvc, initialize_dvc_storage
from pytorch_end_to_end.utils import get_logger

@get_config(config_path="../configs", config_name="config")
def version_data(config: Config) -> None:
    print(config)

    initilaze_dvc_storage(config.dvc_remote_name, config.dvc_remote_url)
    initilaze_dvc()


if __name__ == "__main__":
    version_data()