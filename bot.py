from markov import Markov
from tweet import api
import nltk

text = open('mdpandp.txt')
md = open('md.txt')
pandp = open('pandp.txt')
bot = Markov(text, md, pandp)



if __name__ == "__main__":



    while True:
        with open('tweets.txt', 'a') as tweet_body:
            t = bot.make_tweet()
            print t
                
            post = raw_input("Funny?  ")
            if post == 'y':
    #            api.PostUpdate(t)
                to_save = (t, 'funny')
            else:
                to_save = (t, 'not funny')    
            to_save = str(to_save)       
            tweet_body.write(to_save)
        