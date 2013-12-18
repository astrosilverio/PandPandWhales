from __future__ import division
import random
import string
from itertools import izip
from collections import defaultdict, Counter
import nltk
# import pdb
import math

class Markov(object):

    LOW_NUMBER = 1e-5

    def __init__(self, source_text, text_type='standard'):
        self.corpus = self.get_sentences(source_text, text_type)
        self.unigrams = self.make_unigrams()
        self.word_nums = self.make_word_nums()

        bigram_freqs = self.make_ngram_freqs_dict(2)
        self.bigrams = self.normalize_ngrams(bigram_freqs)

        trigram_freqs = self.make_ngram_freqs_dict(3)
        self.trigrams = self.normalize_ngrams(trigram_freqs)

        self.ngrams = [None, self.unigrams, self.bigrams, self.trigrams]
        
    def get_sentences(self, filename, text_type):
        with open(filename) as f:
            out = f.readlines()

        if text_type == 'standard':
            for line in out:
                line = ["**Beginning**"] + line.strip().split() + ["**End**"]
                line = [word.lstrip('`').rstrip('`') for word in line if word.count('`') % 2 == 1]
        
        elif text_type == 'titles':
            out = [line.strip().split() for line in out]

        return out
        
    def make_word_nums(self):
        out = defaultdict(list)
        for line in self.corpus:
            for i, word in enumerate(line):
                out[i].append(word)
                out[i-len(line)].append(word)
        return out
        
    def make_unigrams(self):
        out = defaultdict(lambda: self.LOW_NUMBER)
        counts = Counter()
        for sent in self.corpus:
            for word in sent:
                counts[word] += 1
        total_words = sum(counts.values())
        for word, count in counts.items():
            out[word] = count / total_words
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
            total_occurences = sum(counts_dict[prev].values())
            for cur in counts_dict[prev]:
                out[prev][cur] = counts_dict[prev][cur] / total_occurences
        return out
        
    def choose_word(self, word_dist):
        score = random.random()    
        for word, prob in word_dist.items():
            if score < prob:
                return word
            score -= prob

    def do_queneau(self):
        length = len(random.choice(self.corpus))
        out = [random.choice(self.word_nums[i]) for i in range(length - 1)]
        out[-1] = random.choice(self.word_nums[-1])
        return self.smart_join(out)
        
         
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
                return self.smart_join(out)
            out.append(cur)
            if n == 2:
                prev = cur
            elif n == 3:
                prev = (prev[1], cur)

    def smart_join(self, token_list):
        out = []
        for token in token_list:
            if token in string.punctuation or token.startswith('//'):
                out.append(token)
            else:
                out.extend([' ', token])
        return "".join(out)
        
                
    def make_post(self):
        post = ""
        while "***END_POST***" not in post:
            sentence = self.make_ngram_sentence(3)
            sentence += random.choice(['','','','\n\n'])
            post += sentence
        post = post[:post.find("***END_POST***")]
        return post

    def score_sentence(self, sent):
        total_surprise = 0
        words = nltk.word_tokenize(sent)
        words = ["**Beginning**"] + words + ["**End**"]
        for w1, w2, cur in izip(words, words[1:], words[2:]):
            if (w1, w2) in self.trigrams and cur in self.trigrams[(w1, w2)]:
                surprise = -math.log(self.trigrams[(w1, w2)][cur], 2)
            elif w2 in self.bigrams and cur in self.bigrams[w2]:
                prob = 0.4 * self.bigrams[w2][cur]
                surprise = -math.log(prob, 2)
            else:
                prob = 0.4 * 0.4 * self.unigrams[cur]
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
        
        bigram_freqs = self.make_ngram_freqs_dict(2)
        self.bigrams = self.normalize_ngrams(bigram_freqs)
        
        trigram_freqs = self.make_ngram_freqs_dict(3)
        self.trigrams = self.normalize_ngrams(trigram_freqs)  
        
        self.ngrams = [None, self.unigrams, self.bigrams, self.trigrams]      
        
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

        tweet = self.make_ngram_sentence()
        is_sent = self.is_sentence(tweet)
        both = self.is_from_both_texts(tweet)
        
        amusing = len(tweet)/140 + is_sent + both
                   
        while len(tweet) > 140 or amusing < 1:
            tweet = self.make_ngram_sentence()
            is_sent = self.is_sentence(tweet)
            both = self.is_from_both_texts(tweet)
            amusing = len(tweet)/140 + is_sent + both

        print amusing, len(tweet), is_sent, both
        return tweet
        