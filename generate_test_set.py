import random

from nltk.corpus import wordnet as wn

N = 50

def main():
    all_synsets = list(wn.all_synsets(wn.NOUN))
    records = random.sample(all_synsets, N)
    print(records)


if __name__ == "__main__":
    main()
