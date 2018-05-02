import collections
import json
import re

import numpy
import matplotlib.pyplot as plot; plot.rcdefaults()
import matplotlib.pyplot as plot

from typing import Tuple


# Common stopwords, mostly taken from the library NLTK
# I've added a few filler words that kept showing up in the graph
STOP_WORDS = ('ourselves', 'd', 'yourself', 'but', 'second', 'go', 'around', 
              'hey', 'girl', 'someone', 'again', 'one', 'two', 'man', 'woman', 
              'get', 'back', 'figure', 'there', 'about', 'once', 'during', 'out', 
              'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 
              'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 
              'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
              'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 
              'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more',
              'himself', 'this', 'down', 'should', 'our', 'their', 'while', 
              'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 
              'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 
              'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 
              'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 
              'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 
              'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 
              'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
              'doing', 'it', 'how', 'further', 'was', 'here', 'than', 'll',
              've', 're', 'm', 'next', 'guy', 'person', 'like', 'first', 'us', 
              'another', 'character', 'still')


def process_text(s: str) -> str:
    """Processes text to remove stopwords and special characters
    
    Args:
        s (str): The string to process
    
    Returns:
        str: The processed text
    """
    # This is a hideous abuse of regex probably, but here's what it does:
    #   \[\[.+?\]\] matches [[]] and any text between
    #   {{.+?}} matches {{}} and any text between
    #   [^a-z \n] more obviously matches the inverse of a-z, spaces, and linebreaks
    # The rest of the syntax groups them () and matches any of the three |
    pattern = re.compile('(\[\[.+?\]\])|({{.+?}})|([^a-z \n])')
    lowered = s.lower()
    stripped = re.sub(pattern, ' ', lowered)
    rm_stopwords = [w for w in stripped.split() if w not in STOP_WORDS]

    return ' '.join(rm_stopwords)


def generate_json():
    """Generates a file (generated.json)
    The file is sorted via comic number and contains the processed text from 
    xkcd comics.
    """
    with open('xkcd_comics.json') as f:
        comics = json.load(f)


    processed_dict = {}
    for comic in comics:
        transcript = process_text(comics[comic]['transcript'])
        if transcript:
            processed_dict[comic] = transcript
        else:
            processed_dict[comic] = process_text(comics[comic]['alt'])

        print(f'Processed comic #{comic}.', end='\r')

    with open('generated.json', 'w') as f:
        json.dump(processed_dict, f, indent=2)

    print(f'\nSuccessfully wrote {len(processed_dict)} comics to file.')


def _count() -> Tuple[str, int]:
    """Counts the occurrences of "significant" words
    
    Returns:
        Tuple[str, int]: The words and their counts respectively
    """
    with open('generated.json') as f:
        d = json.load(f)

    # Joins all the processed text and then counts the individual words
    counter = collections.Counter(' '.join(d.values()).split())

    return counter.most_common(20)


def make_graph(top_words: tuple):
    """Creates and displays a graph using matplotlib

    Note:
        This was mostly taken from here: https://pythonspot.com/matplotlib-bar-chart/
    
    Args:
        top_words (tuple): Tuple[List(str, int)] generated via :func:`_count()`
    """
    objs = [x[0] for x in top_words]
    y_pos = numpy.arange(len(objs))

    data = [x[1] for x in top_words]

    plot.barh(y_pos, data, align='center', alpha=1)
    plot.yticks(y_pos, objs)
    plot.xlabel('Ocurrences')
    plot.title('Word frequency in XKCD comics')

    plot.show()


if __name__ == '__main__':
    generate_json()
    c = _count()
    make_graph(c)
