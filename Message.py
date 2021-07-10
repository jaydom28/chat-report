import logging
import re

from collections import defaultdict, Counter, namedtuple
from threading import Thread


class Message:
    """
    Base class for holding data from a message.
    """
    def __init__(self, sender, text, time_sent=None):
        self.sender = sender
        self.text = text
        self.time_sent = time_sent

    def count(self, keywords):
        """
        Returns a dict representing how many times each keyword appeared in
        the message
        """
        counter = Counter()
        text = self.text.lower()
        for keyword in sorted(keywords, key=len, reverse=True):
            text, count = re.subn(pattern=keyword, repl='', string=text)
            counter[keyword] = count
        return counter

    @classmethod
    def from_readers(cls, file_readers):
        """
        Returns a list of initialized message objects when given a list of
        FileReaders.
        """
        for reader in file_readers:
            reader.read()

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