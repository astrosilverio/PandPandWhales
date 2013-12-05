import random
import string
from itertools import izip
from collections import defaultdict
import nltk
import pdb

class Markov(object):

    def __init__(self, source_text):
        self.two_seeds = defaultdict(list)
        self.source_text = source_text
        self.corpus = self.source_text.read()
        self.words = self.corpus.split()
        self.uppercases = {word for word in self.words if word.istitle()}
        self.propers = self.get_propers()
        self.make_chains()
        
        
    def get_propers(self):

        table = string.maketrans("","")
        no_punct = self.corpus.translate(table, string.punctuation)
        words = set(no_punct.split())
        uppercases = {word.lower() for word in words if word.istitle()}
        propers = uppercases - words
        propers = {word.title() for word in propers}
        return propers
                    
    def make_chains(self):

        for w1, w2, w3 in izip(self.words, self.words[1:], self.words[2:]):
            key = (w1, w2)
            self.two_seeds[key].append(w3)
                
    def make_text(self):
        
        prefixes = ['Mr.', 'Mrs.']
        starters = self.uppercases & self.propers
        start = random.choice(self.words)
        while start.find('.') != -1:
            start = random.choice(self.words)

        seed = self.words.index(start)
        w1, w2 = self.words[seed], self.words[seed + 1]        
        gen_words = [w1.title(), w2]
        
        while w2.find('.') == -1 or w2 in prefixes:
            w1, w2 = w2, random.choice(self.two_seeds[(w1, w2)])
            gen_words.append(w2)
            
        return ' '.join(gen_words)
        
    def is_sentence(self, sentence):
    
        valid_sent = False
        sent_structures = [['N', 'V', 'N'], ['N', 'D', 'N'], ['P', 'V', 'N'], ['P', 'D', 'N']]
        pos = [p[0] for w, p in nltk.pos_tag(nltk.word_tokenize(sentence))]
        print pos
        for structure in sent_structures:
            if valid_sent == True:
                return valid_sent
            s = []
            for i in range(3):
                try:
                    s.append(pos.index(structure[i]))
                    pos.remove(structure[i])
                except:
                    continue
            valid_sent = sorted(s) == s

        return valid_sent
        
        
    def make_tweet(self, length_weight = 0.25, name_weight = 1.0, fun_weight = 0.5, sentence_weight = 3.5):
    
        funny = ['bonnet', 'ball', 'casks', 'ship', 'marry', 'marriage', 'marries', 'married', 'creature', 'sea', 'whale']

        tweet = self.make_text()


                    
        amusing = len(tweet)/140. * 0.25 + len([name for name in self.propers if tweet.count(name)]) + len([thing for thing in funny if tweet.count(thing)]) * 0.5
        while len(tweet) > 140 or amusing < 2:
            tweet = self.make_text()
            amusing = len(tweet)/140. * 0.25 + len([name for name in self.propers if tweet.count(name)]) + len([thing for thing in funny if tweet.count(thing)]) * 0.5
        return tweet
        