import random
import string
from itertools import izip
from collections import defaultdict, Counter
import nltk
# import pdb
import math

class Markov(object):

    LOW_NUMBER = 1e-5

    def __init__(self, source_text):
        self.corpus = self.get_sentences(source_text)
        self.unigrams = self.make_unigrams()
        self.bigram_freqs = self.make_bigram_counts_dict()
        self.bigrams = self.make_bigrams(self.bigram_freqs)
        self.trigram_freqs = self.make_trigram_counts_dict()
        self.trigrams = self.make_trigrams(self.trigram_freqs)
        
    def get_sentences(self, fn):
        with open(fn) as f:
            out = f.readlines()
            out = [["**Beginning**"] + line.strip().split() + ["**End**"] for line in out]
        return out
        
    def make_unigrams(self):
        out = defaultdict(lambda: self.LOW_NUMBER)
        counts = Counter()
        for sent in self.corpus:
            for cur in sent:
                counts[cur] += 1
        total_words = sum(counts.values())
        for word, count in counts.items():
            out[word] = count / float(total_words)
        return out
        
    def make_bigram_counts_dict(self):
        counts_dict = defaultdict(Counter)
        for sent in self.corpus:
            for (prev, cur) in izip(sent, sent[1:]):
                counts_dict[prev][cur] += 1
        return counts_dict
            
    def make_bigrams(self, counts_dict):
        out = defaultdict(lambda: defaultdict(lambda: self.LOW_NUMBER))
        for prev in counts_dict:
            for cur in counts_dict[prev]:
                out[prev][cur] = counts_dict[prev][cur] / float(sum(counts_dict[prev].values()))
        return out
                                
    def make_trigram_counts_dict(self):
        counts_dict = defaultdict(Counter)
        for sent in self.corpus:
            for (prev_prev, prev, cur) in izip(sent, sent[1:], sent[2:]):
                counts_dict[(prev_prev, prev)][cur] += 1
        return counts_dict
        
    def make_trigrams(self, counts_dict):
        out = defaultdict(lambda: defaultdict(lambda: self.LOW_NUMBER))
        for (w1, w2) in counts_dict:
            for cur in counts_dict[(w1, w2)]:
                out[(w1, w2)][cur] = counts_dict[(w1, w2)][cur] / float(sum(counts_dict[(w1, w2)].values()))
        return out
        
    def choose_word(self, word_dist):
        score = random.random()    
        for word, prob in word_dist.items():
            if score < prob:
                return word
            score -= prob
        return False
         
    def make_bigram_sentence(self, bigram_probs_dict=None):
        if not bigram_probs_dict:
            bigram_probs_dict = self.bigrams
        prev = "**Beginning**"
        out = []
        while True:
            cur = self.choose_word(bigram_probs_dict[prev])
            if cur == "**End**":
                return " ".join(out)
            out.append(cur)
            prev = cur
        return False
        
    def make_trigram_sentence(self, trigram_probs_dict=None):
        if not trigram_probs_dict:
            trigram_probs_dict = self.trigrams
        w1 = "**Beginning**"
        w2 = self.choose_word(self.bigrams[w1])
        out = [w2]
        while True:
            cur = self.choose_word(trigram_probs_dict[(w1, w2)])
            if cur == "**End**":
                return " ".join(out)
            out.append(cur)
            w1, w2 = w2, cur
        return False

    def score_sentence(self, sent, trigram_probs=None, bigram_probs=None, unigram_probs=None):
        if not trigram_probs:
            trigram_probs = self.trigrams
        if not bigram_probs:
            bigram_probs = self.bigrams
        if not unigram_probs:
            unigram_probs = self.unigrams
        total_surprise = 0
        words = nltk.word_tokenize(sent)
        words = ["**Beginning**"] + words + ["**End**"]
        for w1, w2, cur in izip(words, words[1:], words[2:]):
            if (w1, w2) in trigram_probs and cur in trigram_probs[(w1, w2)]:
                surprise = -math.log(trigram_probs[(w1, w2)][cur], 2)
            elif w2 in bigram_probs and cur in bigram_probs[w2]:
                prob = 0.4 * bigram_probs[w2][cur]
                surprise = -math.log(prob, 2)
            else:
                prob = 0.4 * 0.4 * unigram_probs[cur]
                surprise = -math.log(prob, 2)
            total_surprise += surprise
        total_surprise /= (len(words) - 2)
        return total_surprise

class DoubleMarkov(Markov):

    LOW_NUMBER = 1e-7

    def __init__(self, text_one, text_two):
        self.text_one = text_one
        self.text_two = text_two
        self.corpus = self.text_one.corpus + self.text_two.corpus
        self.unigrams = self.make_unigrams()
        self.bigram_freqs = self.make_bigram_counts_dict()
        self.bigrams = self.make_bigrams(self.bigram_freqs)
        self.trigram_freqs = self.make_trigram_counts_dict()
        self.trigrams = self.make_trigrams(self.trigram_freqs)        
        
    def get_propers(self, text):

        table = string.maketrans("","")
        no_punct = text.translate(table, string.punctuation)
        words = set(no_punct.split())
        uppercases = {word.lower() for word in words if word.istitle()}
        propers = uppercases - words
        propers = {word.title() for word in propers}
        return propers

    def is_sentence(self, sentence):
    
        words = nltk.word_tokenize(sentence)
    
        valid_sent = False
        pos = [p[0] for w, p in nltk.pos_tag(words)]
        for p1, p2 in izip(pos, pos[1:]):
            if (p1, p2) == ('N', 'V'):
                valid_sent = True
        return valid_sent
        
    def is_from_both_texts(self, sentence):
    
        words = nltk.word_tokenize(sentence)
    
        one = False
        two = False
        for w1, w2 in izip(words, words[1:]):
            if w2 in self.text_one.bigrams[w1] and w2 not in self.text_two.bigrams[w1]:
                one = True
            if w2 in self.text_two.bigrams[w1] and w2 not in self.text_one.bigrams[w1]:
                two = True

        both = one and two
        return both
        
        
    def make_tweet(self):
    
#        funny = ['bonnet', 'ball', 'casks', 'ship', 'marry', 'marriage', 'marries', 'married', 'creature', 'sea', 'whale']

        tweet = self.make_trigram_sentence()
        is_sent = self.is_sentence(tweet)
        both = self.is_from_both_texts(tweet)
        
        amusing = len(tweet)/140. + is_sent + both
                   
        while len(tweet) > 140 or amusing < 1.0:
            tweet = self.make_trigram_sentence()
            is_sent = self.is_sentence(tweet)
            both = self.is_from_both_texts(tweet)
            amusing = len(tweet)/140. + is_sent + both

        print amusing, len(tweet), is_sent, both
        return tweet
        