import os
import sys

from api import (LearnersDictionary, CollegiateDictionary,
                                 WordNotFoundException)
def lookup(dictionary_class, key, query):
    dictionary = dictionary_class(key)
    string = ""
    try:
        defs = [(entry.word, entry.function, definition)
                for entry in dictionary.lookup(query)
                for definition, examples in entry.senses]
    except WordNotFoundException:
        defs = []
    if defs == []:
        return "I couldn't find a definition for: '{0}'".format(query)
    for word, pos, definition in defs:
        string +=  "{0} [{1}]: {2}\n\n".format(word, pos, definition)
        #print string
    string += "http://www.merriam-webster.com/dictionary/{0}".format(word, pos, definition)
    return string


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    learnkey, collkey = (os.getenv("MERRIAM_WEBSTER_LEARNERS_KEY"),
                         os.getenv("MERRIAM_WEBSTER_COLLEGIATE_KEY"))
    if not (learnkey or collkey):
        print ("set the MERRIAM_WEBSTER_LEARNERS_KEY and/or MERRIAM_WEBSTER_"
               "COLLEGIATE_KEY environmental variables to your Merriam-Webster "
               "API keys in order to perform lookups.")
    if learnkey:
        lookup(LearnersDictionary, learnkey, query)
    if collkey:
        lookup(CollegiateDictionary, collkey, query)
