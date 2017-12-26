#1. Iz http://lit.ijs.si/leposl.html pridobi besedilo
#2 Analiziraj pridobljeno besedilo
import urllib.request as url
from bs4 import BeautifulSoup
import re
import collections
import operator


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


def own_probability(input_text, number_of_words):
    #A method that takes the input map/list and calculates the own probability
    #Uses the formula: number of repetitions of a word divided by all words
    all_values= list(input_text.values())
    all_words = list(input_text.keys())
    print(all_values)
    print(all_words)
    own_probs = [x / number_of_words for x in all_values]
    print(own_probs)
    new_dict = dict(zip(all_words, own_probs))
    new_dict = sorted(new_dict.items(), key=operator.itemgetter(1))
    return new_dict


text = get_text()
words = split_text(text)
word_length = len(words)
print(words)
word_count = word_counter(words)
print("Word counter:")
print(word_count)
own_probabilities = own_probability(word_count, word_length)
print("Own probabilities(ascending):")
print(own_probabilities)

