import os
import json
from bs4 import BeautifulSoup
from bs4.element import Comment

def get_file_names(path):
    paths = []
    for file in os.listdir(path):

        if not file.endswith(".json"):
            paths.extend(get_file_names(os.path.join(path, file)))
        else:
            paths.append(os.path.join(path, file))

    return paths


# Code Source https://matix.io/extract-text-from-webpage-using-beautifulsoup-and-python/
def html_to_text(document):
    soup = BeautifulSoup(document, 'html.parser', )
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style'
    ]

    # count = 0
    for t in text:
        if t.parent.name not in blacklist and not isinstance(t, Comment):
            output += '{} '.format(t)

    return output


def get_url_content(path):
    f = open(path, "r")
    data = json.load(f)
    return data['url'], data['content']
