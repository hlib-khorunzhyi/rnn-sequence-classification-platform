from dataclasses import field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass


@dataclass
class DecoderConfig:
    _target_: str = MISSING


@dataclass
class BPEDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.BPEDecoder"
    suffix: str = "</w>"


@dataclass
class ByteLevelDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.ByteLevel"


@dataclass
class CTCDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.CTC"
    pad_token: str = "<pad>"
    word_delimiter_token: str = "|"
    cleanup: bool = True


@dataclass
class FuseDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.Fuse"


@dataclass
class MetaspaceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.Metaspace"
    replacement: str = "_"
    prepend_scheme: str = "always"


@dataclass
class ReplaceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.Replace"
    pattern: str = MISSING
    content: str = MISSING


@dataclass
class SequenceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.Sequence"
    decoders: list[DecoderConfig] = field(default_factory=list)
    _decodess_dict: dict[str, DecoderConfig] = field(default_factory=dict)


@dataclass
class StripDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.Strip"
    content: str = " "
    left: int = 0
    right: int = 0


@dataclass
class WordPieceDecoderConfig(DecoderConfig):
    _target_: str = "tokenizers.decoders.WordPiece"
    prefix: str = "##"
    cleanup: bool = True


def setup_config() -> None:
    cs = ConfigStore.instance()

    cs.store(
        group="tokenization/decoder", name="bpe_decoder_schema", node=BPEDecoderConfig
    )

    cs.store(
        group="tokenization/decoder",
        name="byte_level_decoder_schema",
        node=ByteLevelDecoderConfig,
    )

    cs.store(
        group="tokenization/decoder", name="ctc_decoder_schema", node=CTCDecoderConfig
    )

    cs.store(
        group="tokenization/decoder", name="fuse_decoder_schema", node=FuseDecoderConfig
    )

    cs.store(
        group="tokenization/decoder",
        name="metaspace_decoder_schema",
        node=MetaspaceDecoderConfig,
    )

    cs.store(
        group="tokenization/decoder",
        name="replace_decoder_schema",
        node=ReplaceDecoderConfig,
    )

    cs.store(
        group="tokenization/decoder",
        name="sequence_decoder_schema",
        node=SequenceDecoderConfig,
    )

    cs.store(
        group="tokenization/decoder",
        name="strip_decoder_schema",
        node=StripDecoderConfig,
    )

    cs.store(
        group="tokenization/decoder",
        name="word_piece_decoder_schema",
        node=WordPieceDecoderConfig,
    )
