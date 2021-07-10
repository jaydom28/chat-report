"""
FileReaders can take in a multitude of file types and parse the messages from
them. They should be able to detect a facebook json file among other types.
"""
import json
import logging

from threading import Thread

from Message import FBMessage


class FileReader:
    """
    Base class for reading message data from a file and creating message
    objects.
    """
    def __init__(self, path):
        self.path = path
        self.content = ""
        self.messages = []

    def read(self):
        """
        Return the contents of self.path
        """
        try:
            logging.debug(f'Now scanning {self.path}')
            with open(self.path, "r") as message_file:
                self.content = message_file.read()
        except FileNotFoundError as err:
            self.content = '{}'
            logging.warning(f'Unable to read from {self.path}, file does not exist')

    @classmethod
    def from_strings(cls, file_paths):
        """
        Return a list of initialized FileReader objects.
        """
        return [cls(f_path) for f_path in file_paths]


class FBFileReader(FileReader):
    """
    Reads JSON file containing message data from facebook and creates FBMessage
    objects
    """
    def read(self):
        """
        Creates message objects from message files downloaded from facebook
        """
        super().read()
        file_data = json.loads(self.content)
        if file_data:
            self.messages = [FBMessage(msg) for msg in file_data["messages"]]