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
    word_list = re.split('\n| |\t|,|[(|)]|\.|/|:|–|-', input_text)
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
    own_probs = []
    for x in range(0,len(all_values)):
        own_probs.append(all_values[x] / number_of_words)
    new_dict = dict(zip(all_words, own_probs))
    #Sorting dictionary makes it a list
    return new_dict


def cond_prob(input_text, words):
    #Function that calculates the conditional probability of all words, based on the previous word
    #First we take join the word list by 2 words, ex.: [the,dog,is,cute]->[the dog,dog is,is cute]
    #Then we calculate the conditional probability using the wikipedia equation.
    #P(A|B) = P(AB)/P(B)
    #P(AB) = ex. how many times "the dog" was registered in the text divided by the number of all entries in the text
    #P(B) = own probability of ex. "the"
    #TRY: P(A|B)= P(AB)/P(A)??
    #Then we count how many items the joined words occured in a text
    #Remove empty entries
    all_words = input_text
    joined_words = [None] * (len(all_words)-1)

    for x in range(1, len(all_words)):
        joined_words[x-1] = all_words[x-1] + " " + all_words[x]
    cnt = collections.Counter(map(str.lower,joined_words))
    double_count = cnt
    lowercase_count = double_count.keys()
    #It is irrelevant how many words we have, all that matters is how many times A followed by B occurs and how many times
    double_own = own_probability(double_count, 1)
    own_probs = words

    #Find the first word of each key in double_own and compare it to own_probs, then divide their keys
    divided_list = []

    for key in double_own:
        first_word = key.split()[0]
        if(first_word in own_probs):
            double_value = double_count[key]
            own_value = own_probs[first_word]
            divided_value = double_value / own_value
            divided_list.append(divided_value)

    cond_probs = dict(zip(lowercase_count, divided_list))
    return cond_probs


def uniq_characters(input_text):
    #Firstly we count how many different characters in the text
    #we join the entire text into one word, then check for unique characters using len(set)
    #TODO: Decide if uniq characters is lower case or lower and upper
    one_string = "".join(input_text)
    uniq_chars = len(set(one_string))
    return uniq_chars


def equal_entropy(uniq_chars,length):
    #Function that calculates the entropy of every word, with the condition, THAT EACH WORDS PROBABILITIES ARE EQUAL(THE SAME)
    #Equation used: sum(PROBABILITY *  log(Y)(PROBABILITY)
    #Y = number of unique characters in the alphabet
    probability = 1/length
    logy_probability = math.fabs(math.log(probability, uniq_chars))
    #No for loop needed, because every probability is equal
    return logy_probability


def own_entropy(input_text, uniq_chars):
    #Function that calculates entropy using each word's own probability
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
print(equal_entropy(uniq_characters(words), word_length))
print("Own entropy(ascending):")
own_entropies = own_entropy(own_probabilities, uniq_characters(words))
print(sorted(own_entropies.items(), key=operator.itemgetter(1)))
print("Conditional probabilities:")
print(cond_prob(words, word_count))
