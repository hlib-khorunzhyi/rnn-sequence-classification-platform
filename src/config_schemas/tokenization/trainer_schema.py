from dataclasses import field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, SI
from pydantic.dataclasses import dataclass


@dataclass
class TrainerConfig:
    _target_: str = MISSING
    vocab_size: int | None = None
    show_progress: bool = True
    min_frequency: int = 0
    special_tokens: list[str] | None = field(
        default_factory=lambda: [
            SI("${train_tokenizer.tokenization.unk_token}"),
            SI("${train_tokenizer.tokenization.cls_token}"),
            SI("${train_tokenizer.tokenization.sep_token}"),
            SI("${train_tokenizer.tokenization.pad_token}"),
            SI("${train_tokenizer.tokenization.mask_token}"),
        ]
    )


@dataclass
class BpeTrainerconfig(TrainerConfig):
    _target_: str = "tokenizers.trainers.BpeTrainer"
    vocab_size: int = 30000
    initial_alphabet: list[str] | None = field(default_factory=list)


@dataclass
class UnigramTrainerConfig(TrainerConfig):
    _target_: str = "tokenizers.trainers.UnigramTrainer"
    vocab_size: int = 8000
    initial_alphabet: list[str] | None = field(default_factory=list)
    shrinking_factor: float = 0.75
    unk_token: str | None = SI("${tokenizer.unk_token}")
    max_piece_length: int = 16
    n_sub_iterations: int = 2


@dataclass
class WordLevelTrainerConfig(TrainerConfig):
    _target_: str = "tokenizers.trainers.WordLevelTrainer"


@dataclass
class WordPieceTrainerConfig(TrainerConfig):
    _target_: str = "tokenizers.trainers.WordPieceTrainer"
    vocab_size: int | None = 30000
    limit_alphabet: int | None = None
    initial_alphabet: list[str] | None = field(default_factory=list)
    continuing_subword_prefix: str | None = "##"
    end_of_word_suffix: str | None = None


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenization/trainer", name="bpe_trainer_schema", node=BpeTrainerconfig
    )

    cs.store(
        group="tokenization/trainer",
        name="unigram_trainer_schema",
        node=UnigramTrainerConfig,
    )

    cs.store(
        group="tokenization/trainer",
        name="word_level_trainer_schema",
        node=WordLevelTrainerConfig,
    )

    cs.store(
        group="tokenization/trainer",
        name="word_piece_trainer_schema",
        node=WordPieceTrainerConfig,
    )
