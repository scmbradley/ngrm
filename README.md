# ngrm: A command line anagram generator

## Setup

`ngrm` requires a list of words, separated by new lines,
to work from.
You can download big word lists from here:

- [North America Scrabble Word List](https://www.wordgamedictionary.com/twl06/download/twl06.txt)
- [Europe Scrabble Word List](https://www.wordgamedictionary.com/sowpods/download/sowpods.txt)

You will need to remove the top few header lines from these files:

    $ tail -n +3 twl06.txt > na-wordlist.txt
    $ tail -n +7 sowpods.txt > eu-wordlist.txt

Because I couldn't find out what licenses these word lists are released under, they aren't included in the repository.






