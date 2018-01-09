#1. Iz http://lit.ijs.si/leposl.html pridobi besedilo
#2 Analiziraj pridobljeno besedilo
import re
import collections
import operator
import math

import sys


def get_text():
    #A function that trims out the HTML tags
    #Currently does not trim it all

    try:
        with open("/home/PycharmProjects/pyFormationNEW/source.txt", 'r') as myFile:
            data = myFile.read()
    except IOError:
        print("File error")
    return data


def split_text(input_text):
    #A function that returns an array of words, separated by a space.
    #First it splits the parentheses and dots etc. and then it removes the empty characters
    word_list = re.split('\n| |\t|,|[(|)]|\.|/|:|–|-', input_text)
    word_list = list(filter(None, word_list))
    return word_list


def word_counter(input_text):
    #A method that counts how many times each word has been used and saves it in an array
    #Also makes it all lower case
    return collections.Counter(map(str.lower, input_text))


def own_probability(input_text, number_of_words):
    #A method that takes the input map/list and calculates the own probability
    #Uses the formula: number of repetitions of a word divided by all words
    #number_of_words = number of non-unique words
    #input text = map with amount of repetitions of each word
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
    #TRY: P(A|B)= P(AB)/P(A)??
    #Then we count how many items the joined words occured in a text
    #Remove empty entries
    all_words = input_text
    #joined words is double text, that contains non-unique characters
    #cnt = contains only unique double words and how many times they appear
    #word_count = map with a word and the amount of times it appears
    joined_words = [None] * (len(all_words)-1)

    for x in range(1, len(all_words)):
        joined_words[x-1] = all_words[x-1] + " " + all_words[x]
    cnt = collections.Counter(map(str.lower,joined_words))
    double_count = cnt
    lowercase_count = double_count.keys()
    #It is irrelevant how many words we have, all that matters is how many times A followed by B occurs
    # and how many times A occurs
    double_own = own_probability(double_count, len(joined_words))
    own_probs = words
    #In case all the words are the same, the function under this does not work corectly, for an unknown reason
    if sum(own_probs.values()) is 1:
        return 1.0

    #Find the first word of each key in double_own and compare it to own_probs, then divide their keys
    divided_list = []
    #TODO: if all the words in text are the same, conditional probability is not calculated correctly
    for key in double_own:
        first_word = key.split()[0]
        if first_word in own_probs:
            double_value = double_count[key]
            own_value = own_probs[first_word]
            divided_value = double_value / own_value
            divided_list.append(divided_value)
    cond_probs = dict(zip(lowercase_count, divided_list))
    return cond_probs


def equal_entropy(length, all_length):
    #Function that calculates the entropy of every word, with the condition,
    # THAT EACH WORDS PROBABILITIES ARE EQUAL(THE SAME)
    #PROBABILITY = 1/length
    #Equation used: sum(PROBABILITY *  log(Y)(PROBABILITY)
    #Y = number of unique characters in the alphabet
    #length = how many unique words in the text
    #TODO: Check why entropy wouldnt be 1??
    probability = 1/all_length
    try:
        logy_probability = (math.fabs(math.log(probability, length)))
    except ZeroDivisionError:
        logy_probability = 0
    #No for loop needed, because every probability is equal
    return logy_probability


def own_entropy(input_text, length):
    #Function that calculates entropy using each word's own probability
    #Uses the same formula equal entropy uses, but calculates a different probability
    #Entropy = p * log p
    #TODO: Check if correct calculation
    all_words = list(input_text.keys())
    all_values = list(input_text.values())
    if len(input_text) is 1:
        return 0
    for x in range(0, len(all_values)):
        all_values[x] = (math.fabs(all_values[x] * math.log(all_values[x], length)))
    new_dict = dict(zip(all_words, all_values))
    print("Sum of all entropies")
    entropy = 0.0
    for x in range(0,len(all_values)):
        entropy += all_values[x]
    print(entropy)
    return new_dict


text = get_text()
words = split_text(text)
word_length = len(words)
print("Words:")
print(words)
print("Amount of non-unique words:")
print(len(words))
word_count = word_counter(words)
print("Word counter:")
print(word_count)
print("Amount of unique words:")
print(len(word_count))
own_probabilities = own_probability(word_count, word_length)
print("Own probabilities(ascending):")
print(sorted(own_probabilities.items(), key=operator.itemgetter(1)))
print("Conditional probabilities:")
conditional_probabilities = cond_prob(words,word_count)
print(conditional_probabilities)
print("Unique word pairs:")
print(len(conditional_probabilities))
print("Equal entropy(equal for every word):")
print(equal_entropy(len(word_count),len(words)))
print("Own entropy(ascending):")
own_entropies = own_entropy(own_probabilities,word_length)
print(own_entropies)
print("Conditional entropies:")
print(own_entropy(conditional_probabilities,len(conditional_probabilities)))
