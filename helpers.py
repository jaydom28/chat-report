"""
Helper classes and functions to tidy up the code a little.
"""
import json
import os

def read_messages(file_paths: list, verbose: bool = False) -> list:
    """
    Go through json files containing facebook messages and load them all into
    a list of tuples in the form (sender_name, message_content)

    :file_paths: - a list of strings of paths leading to files containing facebook messages
    :return: - a list of tuples in the form (sender_name, message_content)
    """
    if verbose:
        print("Now reading in the following files:")

    messages = []
    for path in file_paths:
        if not os.path.exists(path):
            print("The following file does not exist:", path)
            exit()
        messages.extend(_read_messages_from_file(path))
        if verbose:
            print(path)

    return messages

def _read_messages_from_fb_json(file_path: str):
    """
    Reads the messages from a json file generated when you download your
    facebook data from the facebook website.
    """
    with open(file_path, "r") as msg_file:
        messages = json.load(msg_file)["messages"]
    return messages

def _read_messages_from_file(file_path: str, file_read_func=_read_messages_from_fb_json) -> list:
    """
    Extract messages from a single file.

    :file_path: - string indicating the path of a file containing messages.
    :return: - a list of tuples in the form (sender_name, message_content)
    """
    return file_read_func(file_path)
