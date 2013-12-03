import random

class Markov(object):

    def __init__(self, source_text):
        self.two_seeds = {}
        self.source_text = source_text
        self.words = self.get_source_words()
        self.make_chains()
        
    def get_source_words(self):
        self.source_text.seek(0)
        words = self.source_text.read().split()
        return words
        
    def k_chains(self, k):
        # only works for k = 3
    
        if len(self.words) < k:
            return
            
        for i in range(len(self.words) - (k - 1)):
            word_seq = []
            for j in range(0, k):
                word_seq.append(self.words[i+j])
            yield tuple(word_seq)
            
    def make_chains(self):
        
        for w1, w2, w3 in self.k_chains(3):
            key = (w1, w2)
            
            if key in self.two_seeds:
                self.two_seeds[key].append(w3)
            
            else:
                self.two_seeds[key] = [w3]
                
    def make_text(self, size = 25):
        
        prefixes = ['Mr.', 'Mrs.']
        uppercase = [word for word in self.words if word.istitle()]
        start = random.choice(uppercase)
        seed = self.words.index(start)
        w1, w2 = self.words[seed], self.words[seed + 1]        
        gen_words = [w1, w2]
        
        while w2.find('.') == -1 or w2 in prefixes:
            w1, w2 = w2, random.choice(self.two_seeds[(w1, w2)])
            gen_words.append(w2)
            
        return ' '.join(gen_words)
        
    def make_tweet(self):
    
        characters = ['Elizabeth', 'Darcy', 'Bennet', 'Jane', 'Lydia', 'Mary', 'Kitty', 'Bingley', 'Ahab', 'Starbuck', 'Queequeg', 'Ishmael', 'Stubb', 'Flask', 'whale', 'Bourgh', 'he', 'she', 'him', 'her', 'Mr.', 'Mrs.', 'Lizzy', 'Collins']
        funny = ['Netherfield', 'Nantucket', 'bonnet', 'ball', 'Pemberly', 'casks', 'ship', 'marry', 'marriage', 'marries', 'married', 'creature', 'sea']
        verbs = ['is', 'was', 'had', 'has', 'have', 'said', 'cried', 'replied']
        
        tweet = self.make_text()
        amusing = len(tweet)/140. * 0.25 + len([name for name in characters if tweet.count(name)]) + len([thing for thing in funny if tweet.count(thing)]) * 0.5 + len([verb for verb in verbs if tweet.count(verb)])*1.5
        while len(tweet) > 140 or amusing < 2:
            tweet = self.make_text()
            amusing = len(tweet)/140. * 0.25 + len([name for name in characters if tweet.count(name)]) + len([thing for thing in funny if tweet.count(thing)]) * 0.5 + len([verb for verb in verbs if tweet.count(verb)])*1.5
        return tweet, amusing
        