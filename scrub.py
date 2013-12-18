import os

def get_posts():
    with open('all_posts.txt','w') as outfile:
        with open('all_titles.txt', 'w') as titlefile:
            for post in os.listdir('posts/'):
                if "day" in post:
                    with open('posts/'+post) as f:
                        text = f.read()
                        
                        title_start = text.find('title: "') + len('title: "')
                        title_end = text[title_start:].find('"') + title_start
                        title = text[title_start:title_end]
                        titlefile.write(title + '\n')

                        text = text[3:] # slice off header start
                        header_end = text.find('---') + 3
                        text = text[header_end:]
                        text = "***START_POST***." + text + "***END_POST***."

                        outfile.write(text)





if __name__ == '__main__':
    get_posts()