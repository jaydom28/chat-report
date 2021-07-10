"""
Helper classes and functions to tidy up the code a little.
"""
from Message import FBMessage
import json
import logging
import re

from FileReader import FBFileReader

from collections import defaultdict, Counter, namedtuple
from threading import Thread


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
    def from_strings(cls, file_paths):
        """
        Return a dict of Person objects initialized from files in file_paths.
        """
        file_readers = FBFileReader.from_strings(file_paths)
        messages = FBMessage.from_readers(file_readers)
        return {name: Person(name, msgs) for (name, msgs) in messages.items()}

    @property
    def words(self):
        """
        A dict that maps words -> word_counts.
        """
        if self._words is None:
            self._words = Counter()
            for msg in self.messages:
                self._words += Counter(msg.text.lower().split())
        return self._words

    @property
    def word_count(self):
        """
        An integer representing the total number of words that the user has
        sent
        """
        if self._word_count is None:
            self._word_count = sum(count for count in self.words.values())
        return self._word_count

    @property
    def char_count(self):
        """
        An integer representing the total number of characters that the user
        has sent
        """
        if self._char_count is None:
            self._char_count = sum(len(msg.text) for msg in self.messages)
        return self._char_count

    @property
    def basic_info(self):
        """
        Returns basic stats as a tuple.
        """
        return STATS(len(self.messages), self.word_count, self.char_count)

    def count(self, keywords):
        """
        Return a Counter object indicating how many times a person has said
        each keyword
        """
        word_counts = Counter()
        for message in self.messages:
            word_counts += message.count(keywords)
        return word_counts


class PersonContainer:
    """
    Keeps track of multiple person objects
    """
    def __init__(self, persons=None):
        self.persons = persons if persons is not None else {}

    @classmethod
    def from_strings(cls, file_paths):
        """
        Initializes a leaderboard object using a list of file paths
        """
        return cls(persons=Person.from_strings(file_paths))

    def add_person(self, person):
        """
        Adds a person object to the dict
        """
        self.persons[person.name] = person

    def count(self, keywords):
        """
        Returns a grand total of each keyword across all persons
        """
        acc = Counter()
        for _, person in self.persons.items():
            acc += person.count(keywords)
        return acc
