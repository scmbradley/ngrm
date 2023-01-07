"""Find anagrams of string."""

from nncounter import NNCounter, SubtractionError
from pathlib import Path
from enum import Enum, auto
from sortedcontainers import SortedList
import re


class AnagramResults(Enum):
    SUCCESS = auto()
    FAIL = auto()
    CONTINUE = auto()


EMPTY_COUNTER = NNCounter()


def counter_positive(ctr):
    return all([v >= 0 for v in ctr.values()])


class AnagramFinder:
    def __init__(self, word_list_location):
        self.word_list = Path(word_list_location).read_text().splitlines()

    @staticmethod
    def sanitise_word(word):
        return re.sub(r"[a-z]", "", word.lower())

    @staticmethod
    def word_in_ctr(in_word, in_ctr):
        try:
            in_ctr - NNCounter(in_word)
        except SubtractionError:
            return False
        return True

    def find(self, input_string):
        sanitised_input = AnagramFinder.sanitise_word(input_string)
        ctr = NNCounter(sanitised_input)
        word_list = self._find_words(ctr)
        return self._find_anagrams(ctr, word_list)

    def _find_anagrams(self, input_ctr, word_list):
        if input_ctr == EMPTY_COUNTER:
            return AnagramResults.SUCCESS
        anagrams = []
        for word in word_list:
            new_ctr = input_ctr - NNCounter(word)
            continuations = self._find_anagrams(new_ctr, word_list)
            word_plus_continuations = [[word] + x for x in continuations]
            anagrams.extend(word_plus_continuations)
        return anagrams

    def _find_words(self, input_ctr, word_list=None):
        if word_list is None:
            word_list = self.word_list
        matching_words = SortedList()
        for word in word_list:
            if AnagramFinder.word_in_ctr(word, input_ctr):
                matching_words.add(word)
        return matching_words
