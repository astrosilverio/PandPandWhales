from markov import Markov
from tweet import api
import nltk

text = open('mdpandp.txt')
bot = Markov(text)



if __name__ == "__main__":

    while True:

        t = bot.make_tweet()
        print t
        x = bot.is_sentence(t)
        print x
        a = raw_input('> ')
        post = raw_input("Funny?  ")
#        if post == 'y':
#            api.PostUpdate(t)