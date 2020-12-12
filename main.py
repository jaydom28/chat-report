"""
The driver to be run and create a statistics report of chat.
"""
import sys

from argparse import ArgumentParser

from helpers import Person

def parse_args(args):
    """
    Parse in arguments that are passed in when invoking the script.

    :args: a list of tokens in string form containing the arguments passed in
    :return: - a namespace object containing the parsed arguments
    """
    parser = ArgumentParser(description="Create a statistics report of a chat.")
    parser.add_argument(dest="files", metavar="files", nargs="+")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")
    return parser.parse_args(args)


if __name__ == "__main__":
    ARGS = parse_args(sys.argv[1:])
    USERS = Person.from_strings(ARGS.files)
    for u in USERS:
        name, mc, wc, cc = u.name, len(u.messages), u.word_count, u.char_count
        print(f'{name}: {mc} messages, {wc} words, {cc} characters')

    # Analyze Messages
    # Create Charts
