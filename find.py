"""Find anagrams of string."""

from nncounter import NNCounter, SubtractionError
from pathlib import Path
from enum import Enum, auto
from sortedcontainers import SortedList, SortedDict
import re
import cProfile


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
        return re.sub(r"\W", "", word.lower())

    @staticmethod
    def word_in_ctr(in_word, in_ctr):
        try:
            in_ctr - NNCounter(in_word)
        except SubtractionError:
            return False
        return True

    @staticmethod
    def add_word_to_lists(in_word, in_list):
        ret = SortedList()
        for elem in in_list:
            new_elem = SortedList([in_word] + elem)
            if new_elem not in ret:
                ret.add(new_elem)
        return ret

    def find(self, input_string):
        sanitised_input = AnagramFinder.sanitise_word(input_string)
        ctr = NNCounter(sanitised_input)
        word_list = self._find_words(ctr)
        return self._find_anagrams(ctr, word_list)

    def findp(self, input_string):
        a = self.find(input_string)
        for ngrm in a:
            print(" ".join(ngrm))
        print(len(a))

    def _find_anagrams(self, input_ctr, word_list):
        anagrams = SortedList()
        for word in word_list:
            new_ctr = input_ctr - word_list[word]
            if new_ctr == EMPTY_COUNTER:
                if [word] not in anagrams:
                    anagrams.add(SortedList([word]))
            else:
                new_wl = self._find_words(new_ctr, word_list)
                # words_after = new_wl.bisect_right(word)
                # if words_after > 0:
                #     words_after -= 1
                # new_wl = new_wl[words_after:]
                if not new_wl:
                    continue
                else:
                    partials = self._find_anagrams(new_ctr, new_wl)
                    if partials is None:
                        continue
                    for a in AnagramFinder.add_word_to_lists(word, partials):
                        if a not in anagrams:
                            anagrams.add(a)
        return anagrams

    def _find_words(self, input_ctr, word_list=None):
        if word_list is None:
            word_list = {word: NNCounter(word) for word in self.word_list}
        matching_words = SortedDict()
        for word in word_list:
            if AnagramFinder.word_in_ctr(word, input_ctr):
                matching_words[word] = word_list[word]
        return matching_words


def team_test():
    a = AnagramFinder("sowpods.txt")
    team_ctr = NNCounter("britneys")
    team_wl = a._find_words(team_ctr)
    return a._find_anagrams(team_ctr, team_wl)


cProfile.run("team_test()")
