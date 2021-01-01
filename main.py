"""
The driver to be run and create a statistics report of chat.
"""
import sys

from argparse import ArgumentParser

from helpers import Leaderboard

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

def display_basic_stats(users):
    for _, u in users.items():
        name, (mc, wc, cc) = u.name, u.basic_info
        print(f'{name:<20}: {mc:<4} messages, {wc:<5} words, {cc:<5} characters')

if __name__ == "__main__":
    ARGS = parse_args(sys.argv[1:])
    keywords = ["hello", "world", "blah"]
    LEADERBOARD = Leaderboard.from_strings(ARGS.files)
    # display_basic_stats(leaderboard.persons)
    print(LEADERBOARD.count(keywords))

    # Analyze Messages
    # Create Charts
