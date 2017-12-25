#1. Iz http://lit.ijs.si/leposl.html pridobi besedilo
#2 Analiziraj pridobljeno besedilo
import urllib.request as url
from bs4 import BeautifulSoup
import re
import collections

def get_text():
    #A function that trims out the HTML tags
    #Currently does not trim it all

    source = "http://lit.ijs.si/leposl.html"
    try:
        html = url.urlopen(source).read()
    except url.URLError :
        print("Not connected")
        sys.exit(0)
    return re.sub('<[^<]+?>', '', ''.join(BeautifulSoup(html, "lxml").findAll(text=True)))


def split_text(input_text):
    #A function that returns an array of words, separated by a space.
    #First it splits the parentheses and dots etc. and then it removes the empty characters
    #Then it deletes the first few array elements, because BeautifulSoup doesnt delete first few HTML tags and last few
    #We also delete -
    word_list = re.split('\n| |\t|,|[(|)]|\.|/|:|–', input_text)
    word_list = list(filter(None, word_list))

    #Remove this if you're using a different site!
    n = 11
    del word_list[:n]
    return word_list

def word_counter(input_text):
    #A method that counts how many times each word has been used and saves it in an array
    #Also makes it all lower case
    return collections.Counter(map(str.lower, input_text))

text = get_text()

words = split_text(text)

print(words)
print(word_counter(words))
