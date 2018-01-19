#1. Iz text filea pridobi besedilo
#2 Analiziraj pridobljeno besedilo
import re
import collections
import math
import sys
import operator
import numpy as np
import os

def get_text():
    try:
        path = input("Full path to text source file: ")
        with open("/home/PycharmProjects/pyFormationNEW/pyFormation/samplesource.txt", 'r') as myFile:
            data = myFile.read()
    except IOError:
        sys.exit(0)
        print("File error")

    return data


def split_text(input_text):
    #A function that returns an array of words, separated by a space.
    #First it splits the parentheses and dots etc. and then it removes the empty characters
    word_list = re.split(r'[^a-zA-Z0-9čžšćđšČŽŠĐĆüÜéÉâÂÁáàÀÅåêÊËëèÈïÏîÎìÌôÔöÖòÒÛûùÙå]', input_text)
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


def bigram(all_words):
    #A function that makes bigrams and returns a
    #Counter object with how many times each bigram appears in a text
    #An own function because we need bigrams for generating words
    #There are no replicates in bigrams!
    joined_words = [None] * (len(all_words)-1)

    for x in range(1, len(all_words)):
        joined_words[x-1] = all_words[x-1] + " " + all_words[x]
    cnt = collections.Counter(map(str.lower,joined_words))
    return cnt
def cond_prob(input_text, words,cnt):
    #Function that calculates the conditional probability of all words, based on the previous word
    #First we take join the word list by 2 words, ex.: [the,dog,is,cute]->[the dog,dog is,is cute]
    #TRY: P(A|B)= P(AB)/P(A)??
    #Then we count how many items the joined words occured in a text
    #Remove empty entries
    #joined words is double text, that contains non-unique characters
    #cnt = contains only unique double words and how many times they appear
    #word_count = map with a word and the amount of times it appears

    double_count = cnt
    lowercase_count = double_count.keys()
    #It is irrelevant how many words we have, all that matters is how many times A followed by B occurs
    # and how many times A occurs
    double_own = own_probability(double_count, len(input_text))
    own_probs = words
    #In case all the words are the same, the function under this does not work corectly, for an unknown reason
    if sum(own_probs.values()) is 1:
        return 1.0

    #Find the first word of each key in double_own and compare it to own_probs, then divide their keys
    divided_list = []
    for keyxd in lowercase_count:
        first_word = keyxd.split()[0]
        if first_word in own_probs:
            double_value = double_count[keyxd]
            own_value = own_probs[first_word]
            divided_value = double_value / own_value
            divided_list.append(divided_value)

    cond_probs = dict(zip(lowercase_count, divided_list))

    return cond_probs


def equal_entropy(all_length):
    #Function that calculates the entropy of every word, with the condition,
    # THAT EACH WORDS PROBABILITIES ARE EQUAL(THE SAME)
    #PROBABILITY = 1/length
    #Equation used: sum(PROBABILITY *  log(Y)(PROBABILITY)
    #Y = number of unique characters in the alphabet
    #length = how many unique words in the text
    probability = 1/all_length
    try:
        logy_probability = (math.fabs(math.log(probability, 2)))
    except ZeroDivisionError:
        logy_probability = 0
    #No for loop needed, because every probability is equal
    return logy_probability


def own_entropy(input_text):
    #Function that calculates entropy using each word's own probability
    #Uses the same formula equal entropy uses, but calculates a different probability
    #Entropy = p * log p
    #Using log base 2, therefore the result is in bits!
    all_words = list(input_text.keys())
    all_values = list(input_text.values())
    if len(input_text) is 1:
        return 0
    for x in range(0, len(all_values)):
        all_values[x] = (math.fabs(all_values[x] * math.log(all_values[x],2)))
    new_dict = dict(zip(all_words, all_values))

    entropy = 0.0
    for x in range(0,len(all_values)):
        entropy += all_values[x]
    print(" - Sum of all entropies: "+str(entropy))
    return new_dict


def first_word_generator(list_words,list_values):
    #normalize
    #TODO: Join with next_word_generator
    probabilities = np.array(list_values).astype(np.float)
    probabilities = probabilities / np.sum(probabilities)
    choiceX = np.random.choice(list_words, p=probabilities)
    choiceX = choiceX.split(" ",1)[0]
    return choiceX

def next_word_generator(first_word,list_words,list_values,limit):
    probabilities = np.array(list_values).astype(np.float)
    probabilities = probabilities / np.sum(probabilities)
    try:
        for x in range(0,limit):
            indices = [i for i, s in enumerate(list_words) if s.startswith(first_word)]
                #ex. between index 14,17 choose one by weighted random,using their values from list_values
                #PROBABILITIES DO NOT SUM TO 1
            temp = probabilities[indices]/np.sum(probabilities[indices])
            if not indices:
                next_word = first_word_generator(list_words,list_values) + " "
                print(next_word)
            else:
                choiceX = np.random.choice(indices, p=temp)
                next_word = list_words[choiceX]
                next_word = next_word.split(" ",1)[1]
                first_word = next_word + " "
                print(first_word)
    except TypeError:
        print("Value Error here")
    return next_word

def word_generator(words,bigrams,limit):
    #A function that generates words using the Markov chain principle!
    #First word is found in the words Counter object, takes the first word(most common)
    #Take first word, then find it in conditional probabilities
    #Check which word most commonly followed first word
    #We put it in a Counter to kind sort it, so we can just look for the first probability
    #when looking for the first word
    #Limit tells us how many words we want to generate
    #count is ordered, meaning the highest probabilities are first
    #find a first word and get the highest probability or count for (word|...)
    #We use Counter because numpy.random.choice doesnt take float into its parametres
    list_words = list(bigrams.keys())
    list_values = list(bigrams.values())
    print("Generated text:")
    first_word = first_word_generator(list_words,list_values)
    first_word = first_word + " "
    #TODO: TEST WORD_GENERATOR SOME MORE
    #choice = rnd.choice(list_words,list_values)
    #we use a numpy array to be able to use a list as indexes,ex. a[0,14,33]
    print(first_word)
    try:
        next_word_generator(first_word,list_words,list_values,limit)
    except IndexError:
        print("Index error")

    return 0

text = get_text()
words = split_text(text)
word_length = len(words)
word_count = word_counter(words)
#word count is a counter with unique WORDS
#words length is just a split text in a list
#In case there's too many words we print them out in a file for easier readability
own_probabilities = own_probability(word_count, word_length)
with open("Own_probs.txt", "w") as text_file:
    print(own_probabilities, file=text_file)
bigrams = bigram(words)
conditional_probabilities = cond_prob(words,word_count,bigrams)
with open("Cond_probs.txt", "w") as text_file:
    print(conditional_probabilities, file=text_file)
print("Equal entropy(equal for every word): " + str(equal_entropy(word_length)))
print("Entropy using the own probabilities")
own_entropies = own_entropy(own_probabilities)
print("Conditional entropy:")
with open("Own_entropies.txt", "w") as text_file:
    print(own_entropies, file=text_file)
cond_entropies = own_entropy(conditional_probabilities)
with open("Cond_entropies.txt", "w") as text_file:
    print(cond_entropies, file=text_file)
print("Amount of non-unique words:")
print(len(words))
print("Amount of unique words:")
print(len(word_count))
print("Unique word pairs:")
print(len(conditional_probabilities))
if len(word_count) < 100 :
    print("Words:")
    print(words)
    print("Word counter:")
    print(word_count)
    print("Own probabilities:")
    print(own_probabilities)
    print("Conditional probabilities:")
    print(conditional_probabilities)
    print("Own entropies[bit]:")
    print(own_entropies)
    print("Conditional entropies[bit]:")
    print(cond_entropies)
print("Word generator")
ordered_word = collections.OrderedDict(word_count.most_common())
limit = int(input("How many words to print out?"))
limit = limit + 1
print(word_generator(own_probabilities,conditional_probabilities,limit))
