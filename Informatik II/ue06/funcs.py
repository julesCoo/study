from typing import Dict


# (I know that type annotations are not necessary, but I find them to be good practice)
def count_letters(s: str, casesensitive=True) -> Dict[str, int]:
    """
    Count letters in a string, which could be a single word or multiple words.
    Non-letter characters are ignored.
    """
    counts = {}
    for letter in s:
        # skip non-letter characters
        if not letter.isalpha():
            continue

        # convert to lowercase if we don't want to distinguish between cases
        if not casesensitive:
            letter = letter.lower()

        # increase the count for this letter
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1

    return counts


def format_counts(counts: Dict[str, int], min_occurances=0, verbose=False) -> str:
    """
    Format the letter count into a string for display.

    In normal mode, each letter is directly followed by its count,
    and each letter-count pair is separated by a space.

    In verbose mode, each letter is on its own line, followed by an equal sign and its count.

    If a letter occurs less than min_occurances times, it is not included in the string.

    (Bonus) the letters are sorted by their count, descending.
    """

    # sort by count
    sorted_counts = sorted(
        counts.items(),
        key=lambda letter_count: letter_count[1],
        reverse=True,
    )

    # drop letters with too few occurances
    sorted_counts = [
        letter_count
        for letter_count in sorted_counts
        if letter_count[1] >= min_occurances
    ]

    if verbose:
        return "\n".join([f"{letter} = {count}" for letter, count in sorted_counts])
    else:
        return " ".join([f"{letter}{count}" for letter, count in sorted_counts])


def merge_counts(counts1: Dict[str, int], counts2: Dict[str, int]) -> Dict[str, int]:
    """
    Merge two letter count dictionaries into one.
    """
    merged = counts1.copy()
    for letter, count in counts2.items():
        if letter in merged:
            merged[letter] += count
        else:
            merged[letter] = count

    return merged
