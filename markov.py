import random
import re
import string
from itertools import izip
from collections import defaultdict

class Markov(object):

    def __init__(self, source_text):
        self.two_seeds = defaultdict(list)
        self.source_text = source_text
        self.corpus = self.source_text.read()
        self.words = self.corpus.split()
        self.propers = self.get_propers()
        self.make_chains()
        
        
    def get_propers(self):

        table = string.maketrans("","")
        no_punct = self.corpus.translate(table, string.punctuation)
        words = set(no_punct.split())
        uppercases = set([word.lower() for word in words if word.istitle()])
        propers = uppercases - words
        return propers
        
#     def k_chains(self, k):
#         # only works for k = 3
#     
#         if len(self.words) < k:
#             return
#             
#         for i in range(len(self.words) - (k - 1)):
#             word_seq = []
#             for j in range(0, k):
#                 word_seq.append(self.words[i+j])
#             yield tuple(word_seq)
            
    def make_chains(self):

        for w1, w2, w3 in izip(self.words, self.words[1:], self.words[2:]):
            key = (w1, w2)
            self.two_seeds[key].append(w3)
                
    def make_text(self, size = 25):
        
        prefixes = ['Mr.', 'Mrs.']
        uppercase = [word for word in self.words if word.istitle()]
        start = random.choice(uppercase)
#        start = random.choice(self.propers)
        seed = self.words.index(start)
#        while seed == -1:
#            start = random.choice(self.propers)
#            seed = self.words.find(start)
        w1, w2 = self.words[seed], self.words[seed + 1]        
        gen_words = [w1, w2]
        
        while w2.find('.') == -1 or w2 in prefixes:
            w1, w2 = w2, random.choice(self.two_seeds[(w1, w2)])
            gen_words.append(w2)
            
        return ' '.join(gen_words)
        
    def make_tweet(self):
    
#        characters = ['Elizabeth', 'Darcy', 'Bennet', 'Jane', 'Lydia', 'Mary', 'Kitty', 'Bingley', 'Ahab', 'Starbuck', 'Queequeg', 'Ishmael', 'Stubb', 'Flask', 'whale', 'Bourgh', 'he', 'she', 'him', 'her', 'Mr.', 'Mrs.', 'Lizzy', 'Collins']
        funny = ['bonnet', 'ball', 'casks', 'ship', 'marry', 'marriage', 'marries', 'married', 'creature', 'sea']

        verbs = ['is', 'was', 'had', 'has', 'have', 'said', 'cried', 'replied']
        
        tweet = self.make_text()
        amusing = len(tweet)/140. * 0.25 + len([name for name in self.propers if tweet.count(name)]) + len([thing for thing in funny if tweet.count(thing)]) * 0.5 + len([verb for verb in verbs if tweet.count(verb)])*1.5
        while len(tweet) > 140 or amusing < 2:
            tweet = self.make_text()
            amusing = len(tweet)/140. * 0.25 + len([name for name in self.propers if tweet.count(name)]) + len([thing for thing in funny if tweet.count(thing)]) * 0.5 + len([verb for verb in verbs if tweet.count(verb)])*1.5
        return tweet, amusing
        