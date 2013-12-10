import unittest
from markov import Markov
import one_sentence_per_line as ospl
import os
from collections import defaultdict

class Test_NGrams(unittest.TestCase):

    def setUp(self):
        self.test_text = "I have bought this bonnet.\r\nI am Mr. Darcy.\r\nI am.\r\n"
        with open("in.txt",'w') as f:
            f.write(self.test_text)
        self.test_outfile = "out.txt"
        ospl.process_data("in.txt", self.test_outfile, True)
        self.test_markov = Markov(self.test_outfile)
    
    def test_unigrams(self):
        self.assertEqual(type(self.test_markov.unigrams), defaultdict)
        self.assertEqual(round(sum(self.test_markov.unigrams.values()), 5), 1.0)
        self.assertEqual(self.test_markov.unigrams["**Beginning**"], 0.15)
    
    def test_bigrams(self):
        self.assertEqual(type(self.test_markov.bigrams), defaultdict)
        self.assertEqual(round(sum(self.test_markov.bigrams["I"].values()), 5), 1.0)
        self.assertEqual(self.test_markov.bigrams["**Beginning**"]["I"], 1.0)
        self.assertEqual(self.test_markov.bigrams["I"]["have"], 1/3.)
    
    def test_bigrams_counter(self):
        bigram_freqs = self.test_markov.make_ngram_freqs_dict(2)
        self.assertEqual(type(bigram_freqs), defaultdict)
        self.assertEqual(bigram_freqs["I"]["am"], 2)
        self.assertEqual(bigram_freqs["."]["**End**"], 3)
        
    def test_trigrams(self):
        self.assertEqual(type(self.test_markov.trigrams), defaultdict)
        self.assertEqual(round(sum(self.test_markov.trigrams[("I","am")].values()), 5), 1.0)
        self.assertEqual(self.test_markov.trigrams[("**Beginning**","I")]["am"], 2/3.)
        self.assertEqual(self.test_markov.trigrams[("I","have")]["rocketships"], 1e-5)

    def test_trigrams_counter(self):
        trigram_freqs = self.test_markov.make_ngram_freqs_dict(3)
        self.assertEqual(type(trigram_freqs), defaultdict)
        self.assertEqual(trigram_freqs[("Darcy",".")]["**End**"], 1)
        self.assertEqual(trigram_freqs[("**Beginning**","I")]["am"], 2)
    
    def tearDown(self):
        os.remove("in.txt")
        os.remove("out.txt")
    

if __name__ == '__main__':

    unittest.main()