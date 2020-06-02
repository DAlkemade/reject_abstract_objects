import random

from nltk.corpus import wordnet as wn

N = 100

def main():
    all_synsets = list(wn.all_synsets(wn.NOUN))
    records = random.sample(all_synsets, N)
    records = [r.name().split('.')[0].replace('_',' ') for r in records]
    with open('test.txt', 'w') as f:
        for item in records:
            f.write(f'{item}\n')



if __name__ == "__main__":
    main()
