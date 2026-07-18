import argparse
from pathlib import Path

from src.utils.config_utils import config_args_parser, compose_config, save_config_as_yaml, save_config_as_pickle


def generate_final_config(args: argparse.Namespace) -> None:
    config_path = args.config_path
    config_name = args.config_name
    overrides = args.overrides

    config = compose_config(config_path, config_name, overrides)

    config_save_dir = Path("./src/configs/automatically_generated")
    config_save_dir.mkdir(parents=True, exist_ok=True)

    save_config_as_yaml(config, str(config_save_dir / f"{config_name}.yaml"))
    save_config_as_pickle(config, str(config_save_dir / f"{config_name}.pickle"))


if __name__ == "__main__":
    generate_final_config(config_args_parser())