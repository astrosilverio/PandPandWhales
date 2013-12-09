import cProfile
from markov import Markov, DoubleMarkov

f = "md_sentences.txt"
g = "pandp_sentences.txt"
a = Markov("md_sentences.txt")
b = Markov("pandp_sentences.txt")

if __name__ == '__main__':

    cProfile.run('Markov(f)')
    cProfile.run('Markov(g)')
    cProfile.run('DoubleMarkov(a,b)')
#    cProfile.run('Markov(f).make_tweet()')