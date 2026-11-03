from dataclasses import field
from typing import Any

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic.dataclasses import dataclass


@dataclass
class WorkerClassConfig:
    pass


@dataclass
class DaskClusterConfig:
    _target_: str = MISSING
    n_workers: int = 1


@dataclass
class LocalDaskClusterConfig(DaskClusterConfig):
    _target_: str = "dask.distributed.LocalCluster"
    memory_limit: str = "auto"
    processes: bool = True
    threads_per_worker: int = 1
    scheduler_port: int = 8786
    host: str | None = None
    dashboard_address: str = ":8787"
    asynchronous: bool = False
    blocked_handlers: list[str] | None = None
    service_kwargs: dict[str, dict[str, Any]] | None = None
    security: bool | None = None
    protocol: str | None = None
    worker_class: WorkerClassConfig | None = None


@dataclass
class GCPDaskClusterConfig(DaskClusterConfig):
    _target_: str = "dask_cloudprovider.gcp.GCPCluster"
    projectid: str = SI("${infrastructure.project_id}")
    zone: str = SI("${infrastructure.zone}")
    network: str = SI("${infrastructure.network}")
    network_projectid: str | None = SI("${infrastructure.project_id}")
    machine_type: str = "n1-standard-1"
    source_image: str = (
        "projects/ubuntu-os-cloud/global/images/family/ubuntu-minimal-2204-lts"
    )
    docker_image: str | None = "daskdev/dask:latest"
    docker_args: str = ""
    extra_bootstrap: list[str] | None = field(
        default_factory=lambda: [
            "gcloud auth configure-docker --quiet europe-west4-docker.pkg.dev"
        ]
    )
    ngpus: int | None = 0
    scheduler_ngpus: int | None = 0
    worker_ngpus: int | None = 0
    filesystem_size: int | None = 50
    disk_type: str | None = "pd-standard"
    on_host_maintenance: str | None = "TERMINATE"
    bootstrap: bool | None = True

    n_workers: int = 0
    worker_class: str = "dask.distributed.Nanny"
    worker_options: dict[str, Any] = field(default_factory=dict)
    env_vars: dict[str, str] = field(default_factory=dict)
    scheduler_options: dict[str, str] = field(default_factory=dict)
    silence_logs: bool | None = None
    asynchronous: bool | None = None
    security: bool = True
    preemptible: bool | None = False
    debug: bool | None = False
    instance_labels: dict[str, str] | None = None


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(
        name="local_dask_cluster_schema",
        node=LocalDaskClusterConfig,
        group="process_data/dask_cluster",
    )
    cs.store(
        name="gcp_dask_cluster_schema",
        node=GCPDaskClusterConfig,
        group="process_data/dask_cluster",
    )
