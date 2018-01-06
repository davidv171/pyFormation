#1. Iz http://lit.ijs.si/leposl.html pridobi besedilo
#2 Analiziraj pridobljeno besedilo
import urllib.request as url
from bs4 import BeautifulSoup
import re
import collections
import operator
import math


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
    all_values = list(input_text.values())
    all_words = list(input_text.keys())
    own_probs = [x / number_of_words for x in all_values]
    print(own_probs)
    new_dict = dict(zip(all_words, own_probs))
    #Sorting dictionary makes it a list
    return new_dict


def cond_prob():
    #TODO: Function that calculates the conditional probability of all words, based on the previous word
    return 0


def uniq_characters(input_text):
    #Firstly we count how many different characters in the text
    #we join the entire text into one word, then check for unique characters using len(set)
    #TODO: Decide if uniq characters is lower case or lower and upper
    one_string = "".join(input_text)
    uniq_chars = len(set(one_string))
    return uniq_chars

def equal_entropy(input_text,uniq_chars,length):
    #Function that calculates the entropy of every word, with the condition, THAT EACH WORDS PROBABILITIES ARE EQUAL(THE SAME)
    #Equation used: sum(PROBABILITY *  log(Y)(PROBABILITY)
    #Y = number of unique characters in the alphabet
    probability = 1/length
    logy_probability = math.fabs(math.log(probability, uniq_chars))
    #No for loop needed, because every probability is equal
    return logy_probability

def own_entropy(input_text,uniq_chars):
    #TODO: Function that calculates entropy using each word's own probability
    #Uses the same formula equal entropy uses, but calculates a different probability
    all_words = list(input_text.keys())
    all_values = list(input_text.values())

    for x in range(0, len(all_values)):
        all_values[x] = (math.fabs(all_values[x] * math.log(all_values[x], uniq_chars)))
    new_dict = dict(zip(all_words, all_values))
    return new_dict


text = get_text()
words = split_text(text)
word_length = len(words)
print("Words:")
print(words)
word_count = word_counter(words)
print("Word counter:")
print(word_count)
own_probabilities = own_probability(word_count, word_length)
print("Own probabilities(ascending):")
print(sorted(own_probabilities.items(), key=operator.itemgetter(1)))
print("Equal entropy:")
print(equal_entropy(word_count, uniq_characters(words), word_length))
print("Own entropy:")
print(own_entropy(own_probabilities, uniq_characters(words)))
