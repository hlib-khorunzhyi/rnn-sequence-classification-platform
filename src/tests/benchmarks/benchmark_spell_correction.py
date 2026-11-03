import argparse
import statistics
import time
from collections.abc import Callable
from importlib import resources

from symspellpy import SymSpell, Verbosity


def initialize_model(
    max_dictionary_edit_distance: int = 2,
    prefix_length: int = 7,
    count_threshold: int = 1,
) -> SymSpell:
    """Initialize SymSpell using the same dictionaries as the project."""

    model = SymSpell(
        max_dictionary_edit_distance,
        prefix_length,
        count_threshold,
    )

    dictionary_path = str(
        resources.files("symspellpy").joinpath("frequency_dictionary_en_82_765.txt")
    )
    bigram_dictionary_path = str(
        resources.files("symspellpy").joinpath(
            "frequency_bigramdictionary_en_243_342.txt"
        )
    )

    if not model.load_dictionary(dictionary_path, 0, 1):
        raise RuntimeError("Could not load SymSpell dictionary.")

    if not model.load_bigram_dictionary(bigram_dictionary_path, 0, 2):
        raise RuntimeError("Could not load SymSpell bigram dictionary.")

    return model


def correct_compound(
    model: SymSpell,
    text: str,
    max_edit_distance: int,
) -> str:
    """Correct the whole text using compound lookup."""

    suggestions = model.lookup_compound(
        text,
        max_edit_distance=max_edit_distance,
    )

    return suggestions[0].term if suggestions else text


def correct_word_by_word(
    model: SymSpell,
    text: str,
    max_edit_distance: int,
) -> str:
    corrected_words = []

    for word in text.split():
        suggestions = model.lookup(
            word,
            Verbosity.TOP,
            max_edit_distance=max_edit_distance,
        )

        if not suggestions:
            corrected_words.append(word)
            continue

        best_suggestion = suggestions[0]

        # Keep the original word if SymSpell considers it correct.
        if best_suggestion.distance == 0:
            corrected_words.append(word)
        else:
            corrected_words.append(best_suggestion.term)

    return " ".join(corrected_words)


def load_texts(file_path: str | None, sample_size: int) -> list[str]:
    """Load one text per line from a file or use demonstration samples."""

    if file_path:
        with open(file_path, encoding="utf-8") as file:
            texts = [line.strip() for line in file if line.strip()]

        return texts[:sample_size]

    print("WARNING: No input file provided. " "Using demonstration texts instead.")

    samples = [
        "I recieved an adress from the custmer yesterday.",
        "This is a simple sentense with a spelling mistake.",
        "The enviroment is very importent for our futuer.",
        "I dont know how to recieve the correct informtion.",
        "Machine lerning models can make predicitons.",
        "The goverment should improve public transport.",
        "I have a problm with my applicaton.",
        "This product has a very good qualitty.",
        "We need to analize the data before training.",
        "The weather is beutiful today.",
    ]

    return samples[:sample_size]


def benchmark_method(
    name: str,
    correction_function: Callable[[SymSpell, str, int], str],
    model: SymSpell,
    texts: list[str],
    max_edit_distance: int,
    repeats: int,
) -> tuple[list[str], list[float]]:
    """Warm up and benchmark one correction method."""

    # Warm-up: exclude the first calls from measurements.
    for text in texts[: min(10, len(texts))]:
        correction_function(model, text, max_edit_distance)

    timings = []
    results = []

    for _ in range(repeats):
        start = time.perf_counter()

        current_results = [
            correction_function(model, text, max_edit_distance) for text in texts
        ]

        elapsed = time.perf_counter() - start
        timings.append(elapsed)
        results = current_results

    print(f"\n{name}")
    print(f"  Median time: {statistics.median(timings):.4f} sec")
    print(f"  Min time:    {min(timings):.4f} sec")
    print(f"  Max time:    {max(timings):.4f} sec")
    print(f"  Throughput:  " f"{len(texts) / statistics.median(timings):.2f} texts/sec")

    return results, timings


def compare_results(
    texts: list[str],
    compound_results: list[str],
    word_results: list[str],
) -> None:
    """Show how often the two approaches produce different outputs."""

    differences = [
        (original, compound, word)
        for original, compound, word in zip(
            texts,
            compound_results,
            word_results,
        )
        if compound != word
    ]

    print("\nResult comparison")
    print(f"  Total texts:       {len(texts)}")
    print(f"  Different results: {len(differences)}")
    print(f"  Same results:      " f"{len(texts) - len(differences)}")

    if differences:
        print("\nExamples of different corrections:")

        for original, compound, word in differences[:10]:
            print(f"\nOriginal:       {original}")
            print(f"Compound:       {compound}")
            print(f"Word by word:   {word}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark SymSpell correction methods."
    )

    parser.add_argument(
        "--input-file",
        type=str,
        default=None,
        help="Text file containing one text per line.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=1000,
        help="Maximum number of texts to benchmark.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Number of benchmark repetitions.",
    )
    parser.add_argument(
        "--max-edit-distance",
        type=int,
        default=2,
        help="Maximum edit distance.",
    )

    args = parser.parse_args()

    if args.sample_size <= 0 or args.repeats <= 0:
        parser.error("--sample-size and --repeats must be positive.")

    texts = load_texts(args.input_file, args.sample_size)

    if not texts:
        raise ValueError("No texts available for benchmarking.")

    print(f"Texts: {len(texts)}")
    print(f"Repeats: {args.repeats}")
    print(f"Max edit distance: {args.max_edit_distance}")

    start = time.perf_counter()
    model = initialize_model(max_dictionary_edit_distance=args.max_edit_distance)
    initialization_time = time.perf_counter() - start

    print(f"Model initialization: {initialization_time:.4f} sec")

    compound_results, compound_timings = benchmark_method(
        name="lookup_compound()",
        correction_function=correct_compound,
        model=model,
        texts=texts,
        max_edit_distance=args.max_edit_distance,
        repeats=args.repeats,
    )

    word_results, word_timings = benchmark_method(
        name="lookup() per word",
        correction_function=correct_word_by_word,
        model=model,
        texts=texts,
        max_edit_distance=args.max_edit_distance,
        repeats=args.repeats,
    )

    compare_results(
        texts,
        compound_results,
        word_results,
    )

    compound_median = statistics.median(compound_timings)
    word_median = statistics.median(word_timings)

    print("\nPerformance comparison")

    if word_median < compound_median:
        print(f"  Word-by-word is " f"{compound_median / word_median:.2f}x faster.")
    elif compound_median < word_median:
        print(f"  Compound is " f"{word_median / compound_median:.2f}x faster.")
    else:
        print("  Both methods have the same median execution time.")


if __name__ == "__main__":
    main()
