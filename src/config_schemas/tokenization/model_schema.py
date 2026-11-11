from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass


@dataclass
class ModelConfig:
    _target_: str = MISSING


@dataclass
class BPEModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.BPE"
    vocab: dict[str, int] | None = None
    merges: list[list[str]] | None = None
    cache_capacity: int = 10000
    dropout: float | None = None
    unk_token: str | None = None
    continuing_subword_prefix: str = ""
    end_of_word_suffix: str = ""
    fuse_unk: bool = False
    byte_fallback: bool = False
    ignore_merges: bool = False


@dataclass
class UnigramModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.Unigram"
    vocab: list[list[str | float]] | None = None
    unk_id: int | None = None
    byte_fallback: bool = False
    alpha: float | None = None
    nbest_size: int | None = None


@dataclass
class WordLevelModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.WordLevel"
    vocab: str | None = None
    unk_token: str | None = None


@dataclass
class WordPieceModelConfig(ModelConfig):
    _target_: str = "tokenizers.models.None"
    vocab: dict[str, int] | None = MISSING
    unk_token: str | None = "[UNK]"
    max_input_chars_per_word: int | None = 100
    continuing_subword_prefix: str | None = "##"


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(group="tokenization/model", name="bpe_model_schema", node=BPEModelConfig)

    cs.store(
        group="tokenization/model", name="unigram_model_schema", node=UnigramModelConfig
    )

    cs.store(
        group="tokenization/model",
        name="word_level_model_schema",
        node=WordLevelModelConfig,
    )

    cs.store(
        group="tokenization/model",
        name="word_piece_model_schema",
        node=WordPieceModelConfig,
    )
