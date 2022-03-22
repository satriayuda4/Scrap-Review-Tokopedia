import pandas as pd
import re
import string
import nltk
#nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Case folding
def lower_case(review):
    for i in range(len(review)):
        print(i)
        review[i] = review[i].lower()
    return review

#number deleting
def num_delete(review):
    for i in range(len(review)):
        review[i] = re.sub(r"\d+", "", review[i])
    return review

#Punctuation deletion
def punc_delete(review): 
    for i in range(len(review)):
        review[i] = review[i].translate(str.maketrans("","",string.punctuation))
    return review

#Deleting whitespace
def whitespace(review):
    for i in range(len(review)): 
        review[i] = review[i].strip()
    return review

# Tokenizing
def tokenize(review):
    for i in range(len(review)): 
        review[i] = review[i].split()
    return review

def tokenize_nltk(review):
    for i in range(len(review)):
        review[i] = nltk.tokenize.word_tokenize(review[i])
    return review

# Filtering
def stopwords_remove(review):
    listStopword =  set(stopwords.words('indonesian'))
    for i in range(len(review)):
        tokens = review[i]
        removed = []
        for t in tokens:
            if t not in listStopword:
                removed.append(t)
        review[i] = removed
    return review

def sastrawi_stopwords(review):
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    for i in range(len(review)):
        stop = stopword.remove(review[i])
        review[i] = nltk.tokenize.word_tokenize(stop)
    return review

#Stemming Bahasa Indonesia
def sastrawi_stemmer(review):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    for i in range(len(review)):
        review[i] = stemmer.stem(review[i])
    return review

def sentence(words):
    sentc = ""
    for i in words:
        sentc += str(i)
        sentc += " "
    return sentc

def sentence_df(review):
    for i in range(len(review)):
        review[i] = sentence(review[i])
    return review

if __name__ == "__main__":
    file_name = 'LG 24MK600'
    df = pd.read_csv('Export/' + file_name + '.csv')
    print(df.head())
    df = df.dropna()
    X = df["Review"]
    X = lower_case(X)
    X = num_delete(X)
    X = tokenize_nltk(X)
    X = stopwords_remove(X)
    X = sentence_df(X)
    X = sastrawi_stopwords(X)
    X = sentence_df(X)
    X = sastrawi_stemmer(X)
    X = whitespace(X)
    X = punc_delete(X)

    review = {'Review' : X}
    data = pd.DataFrame(review)
    #data.to_csv("review-clean2.csv")

    df.to_csv('Preprocessing/' + file_name + "-cleaned-Words.csv")
    #print(df.head())
    print("Pre-processing Finished")

