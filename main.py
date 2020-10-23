"""
The driver to be run and create a statistics report of chat.
"""
import sys

from argparse import ArgumentParser

import helpers

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
    # Read in messages
    MESSAGES = helpers.read_messages(ARGS.files, ARGS.verbose)
    print("There are %d messages" % len(MESSAGES))
    # Analyze Messages
    # Create Charts
