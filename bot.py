from markov import Markov, DoubleMarkov
from tweet import api
import nltk

md = Markov("md_sentences.txt")
pandp = Markov("pandp_sentences.txt")
bot = DoubleMarkov(md, pandp)



if __name__ == "__main__":

    while True:
        with open('tweet_library.txt', 'a') as tweet_body:
            t = bot.make_tweet()
            print t
            words = nltk.word_tokenize(t)
            post = raw_input("Funny?  ")
            if post == 'y':
    #            api.PostUpdate(t)
                to_save = (t, len(t), bot.is_sentence(words), bot.is_from_both_texts(words), bot.score_sentence(words), bot.text_one.score_sentence(words), bot.text_two.score_sentence(words), 'funny')
            else:
                to_save = (t, len(t), bot.is_sentence(words), bot.is_from_both_texts(words), bot.score_sentence(words), bot.text_one.score_sentence(words), bot.text_two.score_sentence(words), 'not funny')    
            to_save = str(to_save) + ',\n'       
            tweet_body.write(to_save)
        