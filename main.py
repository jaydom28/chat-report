"""
The driver to be run and create a statistics report of chat.
"""
import sys
import logging

import Figures

from argparse import ArgumentParser
from matplotlib import pyplot as plt

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
    ARGS = parse_args(sys.argv[1:])
    logging.info(f'Scanning the following files for messages')
    for file_path in ARGS.files:
        logging.info(f'\t{file_path}')

    keywords = ["chink"]
    PERSON_CONTAINER = PersonContainer.from_strings(ARGS.files)
    # display_basic_stats(leaderboard.persons)
    names = [*PERSON_CONTAINER.persons.keys()]

    # Create a pie chart of the total messages sent
    message_counts = [len(person.messages) for person in PERSON_CONTAINER.persons.values()]
    total_messages = sum(message_counts)
    chart_labels = [f'{name} ({msgs/total_messages * 100: .1f}%)' for name, msgs in zip(names, message_counts)]
    chart_title = f'{total_messages} Messages Sent'
    Figures.create_pie_chart(chart_labels, message_counts, title=chart_title, fname="total_message_pie.pdf")

    # Create a pie chart of total words sent
    word_counts = [person.word_count for person in PERSON_CONTAINER.persons.values()]
    total_words = sum(word_counts)
    chart_labels = [f'{name} ({msgs/total_words * 100: .1f}%)' for name, msgs in zip(names, word_counts)]
    chart_title = f'{total_words} Words Typed'
    Figures.create_pie_chart(chart_labels, message_counts, title=chart_title, fname="total_words_pie.pdf")

    # Create a pie chart of total characters sent
    char_counts = [person.char_count for person in PERSON_CONTAINER.persons.values()]
    total_chars = sum(char_counts)
    chart_labels = [f'{name} ({msgs/total_chars * 100: .1f}%)' for name, msgs in zip(names, char_counts)]
    chart_title = f'{total_chars} Characters Typed'
    Figures.create_pie_chart(chart_labels, message_counts, title=chart_title, fname="total_chars_pie.pdf")

    # Analyze Messages
    # Create Charts
