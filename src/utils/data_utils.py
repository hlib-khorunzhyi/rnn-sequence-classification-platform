from pathlib import Path
from subprocess import CalledProcessError
from shutil import rmtree

from utils import get_logger, run_shell_command

DATA_UTILS_LOGGER = get_logger(Path(__file__).name)


def is_dvc_initialized() -> bool:
    return (Path().cwd() / ".dvc").exists()


def initialize_dvc() -> None:
    if is_dvc_initialized():
        DATA_UTILS_LOGGER.info("DVC is already initialized")
        return
    DATA_UTILS_LOGGER.info("Initializing DVC")
    run_shell_command("dvc init")
    run_shell_command("dvc config core.analytics false")
    run_shell_command("dvc config core.autostage true")
    run_shell_command("git add .dvc")
    run_shell_command("git commit -m 'Initialized DVC'")


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:
    if not run_shell_command("dvc remote list"):
        DATA_UTILS_LOGGER.info("Initializing DVC storage")
        run_shell_command(f"dvc remote add -d {dvc_remote_name} {dvc_remote_url}")
        run_shell_command("git add .dvc/config")
        run_shell_command(
            f"git commit -m 'Configured remote storage at: {dvc_remote_url}'"
        )
    else:
        DATA_UTILS_LOGGER.info("DVC storage was already initialized...")


def commit_to_dvc(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    current_version = run_shell_command(
        "git tag --list | sort -t v -k 2 -g | tail -1 | sed 's/v//'"
    ).strip()
    if not current_version:
        current_version = "0"
    
    next_version = f"v{int(current_version)+1}"
    run_shell_command(f"dvc add {dvc_raw_data_folder}")
    run_shell_command("git add .")
    run_shell_command(
        f"git commit -m 'Updated version of the data from v{current_version} to {next_version}'"
    )
    run_shell_command(f"git tag -a {next_version} -m 'Data version {next_version}'")
    run_shell_command(f"dvc push {dvc_raw_data_folder}.dvc --remote {dvc_remote_name}")
    run_shell_command("git push --follow-tags")
    run_shell_command("git push -f --tags")


def make_new_data_version(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    try:
        status = run_shell_command(f"dvc status {dvc_raw_data_folder}.dvc")
        if status == "Data and pipelines are up to date.\n":
            DATA_UTILS_LOGGER.info("Data and pipelines are up to date.")
            return
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)
    except CalledProcessError:
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)


def get_cmd_to_get_raw_data(
        version: str,
        data_local_save_dir: str,
        dvc_remote_repo: str,
        dvc_data_folder: str,
        github_user_name: str,
        github_access_token: str,
) -> str:
    """
    Get shell command to download the data from dvc store

    Parameters
    ----------
    version: str
        data version
    data_local_save_dir: str
        where to save the downloaded data locally
    dvc_remote_repo: str
        dvc repository that holds information about the data
    dvc_data_folder: str
        location where the remote data is stored
    github_user_name: str
        github user name
    github_access_token: str
        github access token

    Returns
    -------
    str
        shell command to download the raw data from dvc store
    """

    without_https = dvc_remote_repo.replace("https://", "")
    dvc_remote_repo = f"https://{github_user_name}:{github_access_token}@{without_https}"

    command = f"dvc get {dvc_remote_repo} {dvc_data_folder} --rev {version} -o {data_local_save_dir}"
    return command


def get_raw_data_with_version(
        version: str,
        data_local_save_dir: str,
        dvc_remote_repo: str,
        dvc_data_folder: str,
        github_username: str,
        github_access_token: str,
) -> None:
    rmtree(data_local_save_dir, ignore_errors=True)
    command = get_cmd_to_get_raw_data(version, data_local_save_dir, dvc_remote_repo, dvc_data_folder, github_username, github_access_token)
    run_shell_command(command)