import logging
import warnings

warnings.filterwarnings(
    "ignore", message="Sending large graph of size.*", category=UserWarning
)

logging.getLogger("distributed.shuffle").setLevel(logging.ERROR)
