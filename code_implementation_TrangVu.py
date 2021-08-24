#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:35:28 2020

@author: trangvu
"""
import numpy as np
from numpy import exp
import pandas as pd


## WRITE CODE IN R OR PYTHON TO IMPLEMENT SOFTMAX FUNCTION.
print("\n1.Write code in python to implement softmax function\n")
print("1.a. Apply softmax function in a predefined vector\n")

#Define the softmax function that takes input as a vector
def softmax(vector_input):
    e = exp(vector_input)
    return e / e.sum()
print("Define softmax function: ", softmax)
#Define the vector
input = [4,8,5,6,2,9,7,6,3]
print("\nDefine input in array format as follow:",input)
# Let's convert list of numbers to a list of probabilities using softmax function
output = softmax(input)
# Report the probabilities result
print("\nAs a result,applying softmax function,the propabilities of the vector is calculated as follow:\n", np.around(output,3))
print("\nSum of the probabilities",output.sum())
print("\n***\n")
print("1.b. Apply softmax function in a predefined matrix\n")
print("Given a matrix X 3x3 we could sum over all elements in the same axis.\n")
X = np.random.normal(0,3,(3,6))
print(X)
print("\nDefine softmax function that take input as matrix: ")
# Define softmax function that takes input as a matrix
def softmax2(matrix_input):
    X_exp = np.exp(matrix_input)
    partition = X_exp.sum(1, keepdims = True)
    return X_exp/ partition 
print(softmax2)
# Apply function on the matrix
X_prob = softmax2(X)
print("\nAs a result,applying softmax function,the propabilities of the matrix is calculated as follow:\n")
print(np.around(X_prob,5))
print("\nSum of the probabilities",X_prob.sum(1))

#######################################################################
## WRITE CODE IN R OR PYTHON TO IMPLEMENT CUSTOMER SENTIMENT ANALYTICS
print("\n**************************************************")
print("**************************************************\n")
print("2.Write code in python to implement customer sentiment analytics:")
df = pd.read_csv("clothing_Reviews.csv")
df.head()

### DATA ANALYSIS###
import nltk
import re
import wordcloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from wordcloud import WordCloud 

#cleaning data, change name of column 
df.columns = ['ID','Clothing_ID','Age','Title','Text','Rating','Recommended_ID','Positive_Feedback_num','Division','Department','Class']

# Create stopword list:
print("\nMost frequently used words in the reviews:\n")
stopwords = set(stopwords.words('english'))
stopwords.update(["br", "href"])
df.Text = df.Text.astype(str)
textt = " ".join(review for review in df.Text)
wordcloud = WordCloud(stopwords=stopwords).generate(textt)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud01.png')
plt.show()

### Classifying Reviews
### Positive reviews will be classified as +1 and negative reviews will be classified as -1
# assign reviews with rating > 3 as positive sentiment
# rating < 3 negative sentiment
# remove rating = 3
df = df[df['Rating'] != 3]
df['sentiment'] = df['Rating'].apply(lambda rating : +1 if rating > 3 else -1)
df.head()

### Split positive and negative sentiment and plot word cloud.
positive = df[df['sentiment'] == 1]
negative = df[df['sentiment'] == -1]

######## WORDCLOUD - Positive Sentiment ###########
# good and great will be removed because they were included in negative sentiment.
#stopwords = set(stopwords.words('english'))
stopwords.update(["br", "href","good","great","dress","top","one","like","color","look"]) 
pos = " ".join(review for review in positive.Text)
wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)
print("\nMost frequently used words in the positive reviews:\n")
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud02.png')
plt.show()

######## WORDCLOUD - Negative Sentiment ###########
df.title = str(df.Title)
neg = " ".join(review for review in negative.Text)
wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
print("\nMost frequently used words in the positive reviews:\n")
plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud03.png')
plt.show()
###### DISTRIBUTION OF REVIEWS WITH SENTIMENT ACROSS DATASET
df['sentimentt'] = df['sentiment'].replace({-1 : 'negative'})
df['sentimentt'] = df['sentimentt'].replace({1 : 'positive'})
print("\nDistribiton of reviews with sentiment across dataset")
df.sentimentt.hist(bins=2, alpha=0.5)

### BUILDING THE MODEL############
### Cleaning the data and remove punctuation from the data. 
def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":",  "!",'"'))
    return final
df['Text'] = df['Text'].apply(remove_punctuation)
df = df.dropna(subset=['Text'])
#df['Title'] = df['Text'].apply(remove_punctuation)
# New dataframe will have two columns - Title of review and sentiment.
dfNew = df[['Text','sentiment']]
print("\nTake a look at the heading of new subset dataset\n")
print(dfNew.head())
#random split train and test data 70% train and 30% test
index = df.index
df['random_number'] = np.random.randn(len(index))
train = df[df['random_number'] <= 0.7]
test = df[df['random_number'] > 0.7]

# Create a bag of words using count vectorizer from Scikit-learn library.

# count vectorizer:
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
train_matrix = vectorizer.fit_transform(train['Text'])
test_matrix = vectorizer.transform(test['Text'])

## Import Logistic Regression. 
# Logistic Regression
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()

### Split target and independent variables
X_train = train_matrix
X_test = test_matrix
y_train = train['sentiment']
y_test = test['sentiment']


### Fit model on data
lr.fit(X_train,y_train)


### Make prediction
predictions = lr.predict(X_test)

# find accuracy, precision, recall
# Test the accuracy of the model
from sklearn.metrics import confusion_matrix,classification_report
new = np.asarray(y_test)
confusion_matrix(predictions,y_test)

print("Below is the classification report of my customer review sentiment model")
print(classification_report(predictions,y_test))



