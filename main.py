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
    USERS = helpers.get_person_objects_from_messages(MESSAGES, ARGS.verbose)
    for u in USERS:
        name = u.name
        msg_count = len(u.messages)
        wc = u.word_count
        cc = u.char_count
        print("%s %d messages %d words %d characters" % (name, msg_count, wc, cc))
    print("%d total messages" % sum(len(u.messages) for u in USERS))
    print("%d total words" % sum(u.word_count for u in USERS))
    print("%d total characters" % sum(u.char_count for u in USERS))
    import json
    with open("sample_data.json", "w") as f:
        blah = [(p.name, p.words) for p in USERS]
        blah = dict(blah)
        f.write(json.dumps(blah, indent=4, sort_keys=True))

    # Analyze Messages
    # Create Charts
