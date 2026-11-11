from dataclasses import field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass


@dataclass
class NormalizerConfig:
    _target_: str = MISSING


@dataclass
class ByteLevelNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.ByteLevel"


@dataclass
class LowercaseNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Lowercase"


@dataclass
class NFCNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFC"


@dataclass
class NFDNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFD"


@dataclass
class NFKCNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFKC"


@dataclass
class NFKDNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.NFKD"


@dataclass
class NmtNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Nmt"


# @dataclass
# class PrecompiledNormalizerConfig(NormalizerConfig):
#     _target_: str = "tokenizers.normalizers.Precompiled"


@dataclass
class ReplaceNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Replace"
    pattern: str = MISSING
    content: str = MISSING


@dataclass
class SequenceNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Sequence"
    normalizers: list[NormalizerConfig] = field(default_factory=list)
    _normalizers_dict: dict[str, NormalizerConfig] = field(default_factory=dict)


@dataclass
class StripNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.Strip"
    left: bool = True
    right: bool = True


@dataclass
class StripAccenstNormalizerConfig(NormalizerConfig):
    _target_: str = "tokenizers.normalizers.StripAccents"
    clean_text: bool | None = True
    handle_chinese_chars: bool | None = True
    strip_accents: bool | None = True
    lowercase: bool | None = True


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenization/tokenization/normalizer",
        name="byte_level_normalizer_schema",
        node=ByteLevelNormalizerConfig,
    )

    cs.store(
        group="tokenization/tokenization/normalizer",
        name="lower_case_normalizer_schema",
        node=LowercaseNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="nfc_normalizer_schema",
        node=NFCNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="nfd_normalizer_schema",
        node=NFDNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="nfkc_normalizer_schema",
        node=NFKCNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="nfkd_normalizer_schema",
        node=NFKDNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="nmt_normalizer_schema",
        node=NmtNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="replace_normalizer_schema",
        node=ReplaceNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="sequence_normalizer_schema",
        node=SequenceNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="stip_normalizer_schema",
        node=StripNormalizerConfig,
    )

    cs.store(
        group="tokenization/normalizer",
        name="strip_accents_normalizer_schema",
        node=StripAccenstNormalizerConfig,
    )
