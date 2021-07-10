"""
The driver to be run and create a statistics report of chat.
"""
import sys
import logging

from argparse import ArgumentParser

from Person import PersonContainer

FORMAT = '%(levelname)-8s [%(filename)-16s:%(lineno)3d] %(message)s'
LOG_LEVEL = logging.DEBUG

logging.basicConfig(format=FORMAT, level=LOG_LEVEL)


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
    logging.info('Starting up tool')
    ARGS = parse_args(sys.argv[1:])
    logging.info(f'Scanning the following files for messages')
    for file_path in ARGS.files:
        logging.info(f'\t{file_path}')

    keywords = ["hello", "world", "blah"]
    PERSON_CONTAINER = PersonContainer.from_strings(ARGS.files)
    # display_basic_stats(leaderboard.persons)
    print(PERSON_CONTAINER.count(keywords))

    # Analyze Messages
    # Create Charts
