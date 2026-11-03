import logging
import socket
import subprocess
from importlib import resources

import symspellpy
from symspellpy import SymSpell, Verbosity


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"[{socket.gethostname()}] {name}")


def run_shell_command(cmd: str) -> str:
    return subprocess.run(
        cmd, text=True, shell=True, check=True, capture_output=True
    ).stdout


class SpellCorrectionModel:
    def __init__(
        self,
        max_dictionary_edit_distance: int = 2,
        prefix_length: int = 7,
        count_threshold: int = 1,
    ) -> None:
        self.max_dictionary_edit_distance = max_dictionary_edit_distance
        self.model = self._initialize_model(prefix_length, count_threshold)

    def _initialize_model(
        self, prefix_length: int, count_threshold: int
    ) -> symspellpy.symspellpy.SymSpell:
        model = SymSpell(
            self.max_dictionary_edit_distance, prefix_length, count_threshold
        )

        dictionary_path = str(
            resources.files("symspellpy").joinpath("frequency_dictionary_en_82_765.txt")
        )
        bigram_dictionary_path = str(
            resources.files("symspellpy").joinpath(
                "frequency_bigramdictionary_en_243_342.txt"
            )
        )

        model.load_dictionary(dictionary_path, 0, 1)
        model.load_bigram_dictionary(bigram_dictionary_path, 0, 2)

        return model

    # def __call__(self, text: str) -> str:
    #     result = self.model.lookup_compound(
    #         text, max_edit_distance=self.max_dictionary_edit_distance
    #     )[0].term

    #     return cast(str, result)

    def __call__(self, text: str) -> str:
        words = text.split()
        corrected_words = []

        for word in words:
            suggestions = self.model.lookup(
                word,
                Verbosity.TOP,
                max_edit_distance=self.max_dictionary_edit_distance,
            )

            corrected_words.append(suggestions[0].term if suggestions else word)

        return " ".join(corrected_words)
