import nltk
import sys
from nltk.tokenize import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

#edit nonterminals 
NONTERMINALS = """
S -> CS | NP VP | VP 
NP -> DP | Adj N | CP | N | N Adv | N DP 
VP -> VP PP | VP DP | VP AN | V Adv | V | VP NP
AN -> Adj N | Adj
DP -> Det N | Det AN | DP PP | Det N N DP | Det N DP | Det DP
PP -> P DP | P N | P AN | P DP Adv
CS -> VP Conj VP | VP Conj NP VP | NP VP Conj VP | NP VP Conj NP VP
"""
#CS stands for complex sentences 

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = []
    sentence = sentence.lower()
    tokens = word_tokenize(sentence)
    for word in tokens:
        if word.isalpha():
            words.append(word)
    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NPs = []
    #print(tree.subtrees)
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            NPs.append(subtree)
    return NPs

if __name__ == "__main__":
    main()
