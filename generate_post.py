from markov import Markov


def make_post():
    m = Markov('all_posts_osplized.txt')
    post = m.make_post()
    return post

def make_title():
    t = Markov('all_titles.txt')
    title = t.make_ngram_sentence(2)
    return title

if __name__ == '__main__':
    print make_post()
    for _ in range(5):
        print make_title()