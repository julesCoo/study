import argparse

from funcs import merge_counts, format_counts, count_letters

# setup the CLI interface
parser = argparse.ArgumentParser(
    description="counts the occurrences of letters in words",
)

# we allow passing any number of words, separated by spaces.
# the nargs="*" argument makes sure that we can pass 0 or more words.
parser.add_argument(
    "word",
    type=str,
    nargs="*",
    help="the word to count the letters in",
)

# the following arguments are all optional.
parser.add_argument(
    "-c",
    "--casesensitive",
    action="store_true",
    help="count lower and upper case letters separately",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    help="increase output verbosity each time it is passed",
)
parser.add_argument(
    "--min",
    type=int,
    default=0,
    help="minimum number of occurrences to be considered",
)

# parse arguments into variables
args = parser.parse_args()
words = args.word
casesensitive = args.casesensitive
min_occurances = args.min
verbose = args.verbose > 0
very_verbose = args.verbose > 1

# we need to keep track of the total counts for all words
total_counts = {}

for word in args.word:
    # count the letters in this word and update the total counts.
    # note that there is an inconsistency in the requirements document in whether the minimum
    # check should be applied before or after merging. I chose to apply it before merging.
    word_counts = count_letters(word, casesensitive)
    total_counts = merge_counts(total_counts, word_counts)

    # print the word (only in verbose mode and if it has any letters with enough occurrences)
    if verbose:
        word_count_str = format_counts(word_counts, min_occurances, very_verbose)
        if word_count_str != "":
            print(f"Word: {word}")
            print(word_count_str)


# print the total count
total_count_str = format_counts(total_counts, min_occurances, very_verbose)

if verbose:
    print("Overall count")
print(total_count_str)
