"""
Helper classes and functions to tidy up the code a little.
"""
import json
import os

class Person():
    """
    The Person class contains message data of a particular user as well as
    methods that facilitate getting particular data.
    """
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.words = {}
        self.out_reacts = {} # Reactions this person has given to others
        self.in_reacts = {} # Reactions this person has received on their messages
        self._word_count = None
        self._char_count = None

    def __str__(self):
        return self.name

    @property
    def word_count(self):
        """
        An integer representing the total number of words that the user has sent
        """
        if self._word_count is None:
            if self.words == {}:
                self._initialize_word_counts()
            self._word_count = sum(x for x in self.words.values())
        return self._word_count

    @property
    def char_count(self):
        """
        An integer representing the total number of characters that the user has sent
        """
        if self._char_count is None:
            if self.words == {}:
                self._initialize_word_counts()
            self._char_count = sum([len(word) * count for (word, count) in self.words.items()])
        return self._char_count

    def _initialize_word_counts(self):
        for msg in self.messages:
            for word in msg["content"].split():
                self.words[word] = self.words.get(word, 0) + 1
    
    def _initialize_in_reacts(self):
        for msg in self.messages:
            if "reactions" in msg:
                for react in msg["reactions"]:
                    self.in_reacts[react["reaction"]] = self.in_reacts.get(react["reaction"], 0) + 1

    def get_word_count(self, word: str) -> int:
        """
        Get the number of times the user has said a particular word

        :word: - a string of the word to get a count for
        :return: - an integer, number of times the word has been typed
        """
        if self.words == {}:
            self._initialize_word_counts()
        return self.words.get(word, 0)



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
            print("\t" + path)

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

def get_person_objects_from_messages(messages: list, verbose=False) -> list:
    """
    Create a list of Person objects from a list of messages.

    :messages: - a list of dicts representing messages, must contain "content"
                 and "sender_name" keys
    :return: - a list of Person objects with their messages initialized
    """
    if verbose:
        print("Now creating person objects from the messages.")

    person_objects = {}
    for msg in messages:
        if msg["sender_name"] not in person_objects:
            person_objects[msg["sender_name"]] = Person(msg["sender_name"])
        if "content" in msg:
            msg["content"] = "".join([c.lower() for c in msg["content"] if c.isalnum() or c.isspace()])
            person_objects[msg["sender_name"]].messages.append(msg)
        if "reactions" in msg:
            for reaction in msg["reactions"]:
                actor = reaction["actor"]
                action = reaction["reaction"]
                if actor not in person_objects:
                    person_objects[actor] = Person(actor)
                person_objects[actor].out_reacts[action] = \
                    person_objects[actor].out_reacts.get(action, 0) + 1

    max_name_len = max([len(p.name) for p in person_objects.values()])
    max_dig_len = max([len(str(len(p.messages))) for p in person_objects.values()])

    if verbose:
        output_str = "%%%ds : %%%dd messages" % (max_name_len, max_dig_len)
        for name, p_obj in person_objects.items():
            print(output_str % (name, len(p_obj.messages)))
    return list(person_objects.values())
