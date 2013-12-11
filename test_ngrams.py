from __future__ import division
import unittest
from markov import Markov, DoubleMarkov
import one_sentence_per_line as ospl
import os
from collections import defaultdict

class Test_Markov(unittest.TestCase):

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
        
    def test_make_sentence(self):
        self.test_markov.make_ngram_sentence(n=2)
        self.test_markov.make_ngram_sentence(n=3)
        self.assertRaises(AssertionError, self.test_markov.make_ngram_sentence, n=5)
        
    def test_score_sentence(self):
        """ make up nonsense sentence, make sure it scores worse than Markov sentence. possibly also make up word with same words as corpus but in a completly bogus order, that should also score lower"""
        nonsense = "Vestiges of cetaceous gentility."
        nonsense_score = self.test_markov.score_sentence(nonsense)
        real_trigram_sent = self.test_markov.make_ngram_sentence()
        real_trigram_score = self.test_markov.score_sentence(real_trigram_sent)
        weird_order = "Darcy . I bonnet am bought have am"
        weird_order_score = self.test_markov.score_sentence(weird_order)
        self.assertGreater(nonsense_score, real_trigram_score)
        self.assertGreater(weird_order_score, real_trigram_score)
        
    def tearDown(self):
        os.remove("in.txt")
        os.remove("out.txt")
        

class Test_DoubleMarkov(unittest.TestCase):

    def setUp(self):
        self.test_text_one = "I have bought this bonnet.\r\nI am Mr. Darcy.\r\nI am.\r\n"
        with open("in_one.txt",'w') as f:
            f.write(self.test_text_one)
        self.test_outfile_one = "out_one.txt"
        ospl.process_data("in_one.txt", self.test_outfile_one, True)
        self.test_markov_one = Markov(self.test_outfile_one)
        
        self.test_text_two = "Stubb is whale.\r\nStarbuck is THE whale.\r\nI am a porpoise.\r\n"
        with open("in_two.txt",'w') as f:
            f.write(self.test_text_two)
        self.test_outfile_two = "out_two.txt"
        ospl.process_data("in_two.txt", self.test_outfile_two, True)
        self.test_markov_two = Markov(self.test_outfile_two)
        
        self.test_markov = DoubleMarkov(self.test_markov_one, self.test_markov_two)
        
    def test_unigrams(self):
        self.assertEqual(type(self.test_markov.unigrams), defaultdict)
        self.assertEqual(round(sum(self.test_markov.unigrams.values()), 5), 1)
        self.assertEqual(self.test_markov.unigrams["**Beginning**"], 0.15)
    
    def test_bigrams(self):
        self.assertEqual(type(self.test_markov.bigrams), defaultdict)
        self.assertEqual(round(sum(self.test_markov.bigrams["I"].values()), 5), 1.0)
        self.assertEqual(self.test_markov.bigrams["**Beginning**"]["I"], 2/3)
        self.assertEqual(self.test_markov.bigrams["I"]["have"], 1/4)
    
    def test_bigrams_counter(self):
        bigram_freqs = self.test_markov.make_ngram_freqs_dict(2)
        self.assertEqual(type(bigram_freqs), defaultdict)
        self.assertEqual(bigram_freqs["I"]["am"], 3)
        self.assertEqual(bigram_freqs["."]["**End**"], 6)
        
    def test_trigrams(self):
        self.assertEqual(type(self.test_markov.trigrams), defaultdict)
        self.assertEqual(round(sum(self.test_markov.trigrams[("I","am")].values()), 5), 1.0)
        self.assertEqual(self.test_markov.trigrams[("**Beginning**","I")]["am"], 3/4.)
        self.assertEqual(self.test_markov.trigrams[("I","have")]["rocketships"], 1e-7)

    def test_trigrams_counter(self):
        trigram_freqs = self.test_markov.make_ngram_freqs_dict(3)
        self.assertEqual(type(trigram_freqs), defaultdict)
        self.assertEqual(trigram_freqs[("Darcy",".")]["**End**"], 1)
        self.assertEqual(trigram_freqs[("**Beginning**","I")]["am"], 3)
        
    def test_make_sentence(self):
        self.test_markov.make_ngram_sentence(n=2)
        self.test_markov.make_ngram_sentence(n=3)
        self.assertRaises(AssertionError, self.test_markov.make_ngram_sentence, n=5)
        
    def test_score_sentence(self):
        """ make up nonsense sentence, make sure it scores worse than Markov sentence. possibly also make up word with same words as corpus but in a completly bogus order, that should also score lower"""
        nonsense = "Vestiges of cetaceous gentility."
        nonsense_score = self.test_markov.score_sentence(nonsense)
        real_trigram_sent = self.test_markov.make_ngram_sentence()
        real_trigram_score = self.test_markov.score_sentence(real_trigram_sent)
        weird_order = "Darcy . I bonnet am bought have am"
        weird_order_score = self.test_markov.score_sentence(weird_order)
        self.assertGreater(nonsense_score, real_trigram_score)
        self.assertGreater(weird_order_score, real_trigram_score)
        
    def test_make_tweet(self):
        test_tweet = self.test_markov.make_tweet()
        self.assertGreaterEqual(140, len(test_tweet))
        
    def test_is_sentence(self):
        sentence = "My name is whale."
        not_sentence = "The the the the the."
        self.assertTrue(self.test_markov.is_sentence(sentence))
        self.assertFalse(self.test_markov.is_sentence(not_sentence))
        
    def test_is_from_both_texts(self):
        is_both = "Mr. Darcy is a porpoise."
        not_both = "I have bought a bonnet."
        self.assertTrue(self.test_markov.is_from_both_texts(is_both))
        self.assertFalse(self.test_markov.is_from_both_texts(not_both))
        
    def tearDown(self):
        os.remove("in_one.txt")
        os.remove("out_one.txt")
        os.remove("in_two.txt")
        os.remove("out_two.txt")

if __name__ == '__main__':

    unittest.main()