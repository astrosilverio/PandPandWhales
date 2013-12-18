from markov import Markov
import string

POST_TEMPLATE = """\
---
layout: post
title: %s
---

%s
"""

def make_titles():
    t = Markov('all_titles.txt', text_type='titles')
    titles = []
    for day in range(46):
        title = t.do_queneau()
        titles.append("Day %s: %s" % (day + 1, title))
    return titles

def construct_file(title, post_text):
    filename = title_to_filename(title)
    directory = "fake_posts/"
    with open(directory+filename, 'w') as f:
        f.write(POST_TEMPLATE % (title, post_text))

def title_to_filename(title):
    scrubbed_title = "".join(c for c in title if c not in string.punctuation)
    filename = "-".join(scrubbed_title.split(" ")) + '.md'
    return filename

if __name__ == '__main__':
    m = Markov('all_posts_osplized.txt')
    titles = make_titles()

    for title in titles:
        post = m.make_post()
        construct_file(title, post)