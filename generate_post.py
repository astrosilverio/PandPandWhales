from markov import Markov
import string
import datetime
import pdb

POST_TEMPLATE = """\
---
layout: post
title: "%s"
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

def construct_file(title, post_text, day):
    filename = title_to_filename(title, day)
    directory = "fake_posts/"
    with open(directory+filename, 'w') as f:
        f.write(POST_TEMPLATE % (title, post_text))

def dates():
    one_day = datetime.timedelta(days=1)
    weekend = datetime.timedelta(days=3)
    d = datetime.date(2013,9,30)
    dates = []
    for week in range(12):
        for day in range(4):
            dates.append(d)
            d += one_day
        d += weekend

    dates.remove(datetime.date(2013,11,27))
    dates.remove(datetime.date(2013,11,28))

    dates = [str(date) for date in dates]
    assert len(dates) == 46

    return dates



def title_to_filename(title, date):
    title = "".join(c for c in title if c not in string.punctuation)
    title = "-".join(title.lower().split(" ")) + '.markdown'
    filename = "%s-%s" % (date, title)
    return filename

if __name__ == '__main__':
    dates = dates()
    m = Markov('all_posts_osplized.txt')
    titles = make_titles()

    for title, day in zip(titles, dates):
        post = m.make_post()
        construct_file(title, post, day)
