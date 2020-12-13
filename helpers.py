"""
Helper classes and functions to tidy up the code a little.
"""
import json

from collections import defaultdict, Counter, namedtuple
from threading import Thread

class FileReader:
    """
    Base class for reading message data from a file and creating message objects.
    """
    def __init__(self, path):
        self.path = path
        self.content =""
        self.messages = []

    def read(self):
        """
        Return the contents of self.path
        """
        with open(self.path, "r") as message_file:
            self.content = message_file.read()

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
        self.messages = [FBMessage(msg) for msg in file_data["messages"]]


class Message:
    """
    Base class for holding data from a message.
    """
    def __init__(self, sender, text, time_sent=None):
        self.sender = sender
        self.text = text
        self.time_sent = time_sent

    @classmethod
    def from_readers(cls, file_readers):
        """
        Returns a list of initialized message objects when given a list of readers.
        """
        threads = [Thread(target=r.read) for r in file_readers]
        for thread in threads: thread.start()
        for thread in threads: thread.join()

        name_msg_dict = defaultdict(list)
        for reader in file_readers:
            for msg in reader.messages:
                name_msg_dict[msg.sender].append(msg)
        return name_msg_dict


class FBMessage(Message):
    """
    Holds data for a single facebook message.
    """
    def __init__(self, msg_dict):
        sender = msg_dict.get("sender_name", "")
        text = msg_dict.get("content", "")
        time_sent = msg_dict.get("timestamp_ns", None)
        super().__init__(sender=sender, text=text, time_sent=time_sent)

STATS = namedtuple("stats", ("messages_sent", "word_count", "char_count"))

class Person:
    """
    The Person class contains message data of a particular user as well as
    methods that facilitate getting particular data.
    """
    def __init__(self, name, messages=None):
        self.name = name
        self.messages = messages if messages is not None else []
        self._words = None
        self._word_count = None
        self._char_count = None

    @classmethod
    def from_strings(cls, file_paths, initialized=False):
        """
        Return a dict of Person objects initialized from files in file_paths.
        """
        file_readers = FBFileReader.from_strings(file_paths)
        messages = Message.from_readers(file_readers)
        return [Person(name, msgs) for (name, msgs) in messages.items()]

    @property
    def words(self):
        """
        A dict that maps words -> word_counts.
        """
        if self._words is None:
            self._words = Counter()
            for msg in self.messages:
                self._words += Counter(msg.text.split())
        return self._words

    @property
    def word_count(self):
        """
        An integer representing the total number of words that the user has sent
        """
        if self._word_count is None:
            self._word_count = sum(count for count in self.words.values())
        return self._word_count

    @property
    def char_count(self):
        """
        An integer representing the total number of characters that the user has sent
        """
        if self._char_count is None:
            self._char_count = sum(len(msg.text) for msg in self.messages)
        return self._char_count
    
    @property
    def basic_info(self):
        return STATS(len(self.messages), self.word_count, self.char_count)
