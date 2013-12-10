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

        bigram_freqs = self.make_ngram_freqs_dict(2)
        self.bigrams = self.normalize_ngrams(bigram_freqs)

        trigram_freqs = self.make_ngram_freqs_dict(3)
        self.trigrams = self.normalize_ngrams(trigram_freqs)

        self.ngrams = [None, self.unigrams, self.bigrams, self.trigrams]
        
    def get_sentences(self, filename):
        with open(filename) as f:
            out = f.readlines()
            out = [["**Beginning**"] + line.strip().split() + ["**End**"] for line in out]
        return out
        
    def make_unigrams(self):
        out = defaultdict(lambda: self.LOW_NUMBER)
        counts = Counter()
        for sent in self.corpus:
            for word in sent:
                counts[word] += 1
        total_words = sum(counts.values())
        for word, count in counts.items():
            out[word] = count / float(total_words)
        return out
        
    def make_ngram_freqs_dict(self, n):
        """ Output for n = 2: {'white': {'whale': 9, 'expanse': 1}}"""
        counts_dict = defaultdict(Counter)
        if n == 2:
            sent_zip = lambda sent: izip(sent, sent[1:])
            ngram_key = lambda tup: tup[0]
        elif n == 3:
            sent_zip = lambda sent: izip(sent, sent[1:], sent[2:])
            ngram_key = lambda tup: tup[:2]
        for sent in self.corpus:
            for ngram in sent_zip(sent):
                target = ngram[-1]
                key = ngram_key(ngram)
                counts_dict[key][target] += 1
        return counts_dict
            
    def normalize_ngrams(self, counts_dict):
        """
        e.g., for bigrams:
        Input: {('white',): {'whale': 9, 'expanse': 1}}
        Output: {('white'): {'whale': .9, 'expanse': .1}}
        `prev` key is a word for bigrams and a tuple for trigrams.
        """
        out = defaultdict(lambda: defaultdict(lambda: self.LOW_NUMBER))
        for prev in counts_dict:
            total_occurences = float(sum(counts_dict[prev].values()))
            for cur in counts_dict[prev]:
                out[prev][cur] = counts_dict[prev][cur] / total_occurences
        return out
        
    def choose_word(self, word_dist):
        score = random.random()    
        for word, prob in word_dist.items():
            if score < prob:
                return word
            score -= prob
         
    def make_ngram_sentence(self, n=3):
        assert n in (2,3)
        ngram_probs_dict = self.ngrams[n]
        if n == 2:
            prev = "**Beginning**"
            out = []
        elif n == 3:
            first = self.choose_word(self.bigrams["**Beginning**"])
            prev = ("**Beginning**", first)
            out = [first]
        while True:
            cur = self.choose_word(ngram_probs_dict[prev])
            if cur == "**End**":
                return " ".join(out)
            out.append(cur)
            if n == 2:
                prev = cur
            elif n == 3:
                prev = (prev[1], cur)

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
        