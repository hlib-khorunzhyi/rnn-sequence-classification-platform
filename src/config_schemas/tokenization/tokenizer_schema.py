from hydra.core.config_store import ConfigStore
from omegaconf import MISSING
from pydantic.dataclasses import dataclass

import src.config_schemas.tokenization.decoder_schema as decoder_schemas
import src.config_schemas.tokenization.model_schema as model_schemas
import src.config_schemas.tokenization.normalizer_schema as normalizer_schemas
import src.config_schemas.tokenization.post_processor_schema as post_processor_schemas
import src.config_schemas.tokenization.pre_tokenizer_schema as pre_tokenizer_schemas
import src.config_schemas.tokenization.trainer_schema as trainer_schemas


@dataclass
class TokenizerConfig:
    _target_: str = MISSING


@dataclass
class HuggingFaceTokenizerConfig(TokenizerConfig):
    _target_: str = "src.tokenization.tokenizers.HuggingFaceTokenizer"
    pre_tokenizer: pre_tokenizer_schemas.PreTokenizerConfig = MISSING
    model: model_schemas.ModelConfig = MISSING
    trainer: trainer_schemas.TrainerConfig = MISSING
    normalizer: normalizer_schemas.NormalizerConfig | None = None
    decoder: decoder_schemas.DecoderConfig | None = None
    post_processor: post_processor_schemas.PostProcessorConfig | None = None

    unk_token: str | None = "[UNK]"
    cls_token: str | None = "[CLS]"
    sep_token: str | None = "[SEP]"
    pad_token: str | None = "[PAD]"
    mask_token: str | None = "[MASK]"


def setup_config() -> None:
    normalizer_schemas.setup_config()
    post_processor_schemas.setup_config()
    pre_tokenizer_schemas.setup_config()
    model_schemas.setup_config()
    trainer_schemas.setup_config()
    decoder_schemas.setup_config()

    cs = ConfigStore.instance()

    cs.store(
        group="tokenization",
        name="hugging_face_tokenizer_schema",
        node=HuggingFaceTokenizerConfig,
    )
