from __future__ import print_function, division
from future.utils import iteritems
from builtins import range


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from wordcloud import WordCloud


# data from:
# https://www.kaggle.com/uciml/sms-spam-collection-dataset
# file contains some invalid chars
# depending on which version of pandas you have
# an error may be thrown
df = pd.read_csv('utkmls2/train.csv', encoding='ISO-8859-1')

# drop unnecessary columns
# df = df.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
# df = df.drop(["following", "followers", "actions", "is_retweet", "location"], axis=1)

# print(df)

# rename columns to something better
# df.columns = ['labels', 'data']

# create binary labels
# df['b_labels'] = df['labels'].map({'ham': 0, 'spam': 1})
# Y = df['b_labels'].values
df['b_labels'] = df['Type'].map({'Quality': 0, 'Spam': 1})
Y = df['b_labels'].values

print(Y[Y == 1 ].size)
print(Y[Y == 0 ].size)
print(Y.size)

# check NaN inputs
# print(df['b_labels'].isnull().values.any())
# print(df.loc[pd.isna(df['b_labels']), :].index)

# split up the data
# df_train, df_test, Ytrain, Ytest = train_test_split(df['data'], Y, test_size=0.33)
df_train, df_test, Ytrain, Ytest = train_test_split(df['Tweet'], Y, test_size=0.33)

# try multiple ways of calculating features
# tfidf = TfidfVectorizer(decode_error='ignore')
# Xtrain = tfidf.fit_transform(df_train)
# Xtest = tfidf.transform(df_test)

count_vectorizer = CountVectorizer(decode_error='ignore')
Xtrain = count_vectorizer.fit_transform(df_train)
Xtest = count_vectorizer.transform(df_test)



# create the model, train it, print scores
model = MultinomialNB()
model.fit(Xtrain, Ytrain)

# print out accuracy
print("train score:", model.score(Xtrain, Ytrain)) # accuracy
print("test score:", model.score(Xtest, Ytest))
# exit()


# visualize the data
def visualize(label):
  words = ''
  for msg in df[df['Type'] == label]['Tweet']:
    msg = msg.lower()
    words += msg + ' '
  wordcloud = WordCloud(width=600, height=400).generate(words)
  plt.imshow(wordcloud)
  plt.axis('off')
  plt.show()

# visualize('Spam')
# visualize('Quality')


# # see what we're getting wrong
# X = tfidf.transform(df['data'])
# df['predictions'] = model.predict(X)

# # things that should be spam
# sneaky_spam = df[(df['predictions'] == 0) & (df['b_labels'] == 1)]['data']
# for msg in sneaky_spam:
#   print(msg)

# # things that should not be spam
# not_actually_spam = df[(df['predictions'] == 1) & (df['b_labels'] == 0)]['data']
# for msg in not_actually_spam:
#   print(msg)


# predict another dataset
# df = pd.read_csv('utkmls2/test.csv', encoding='ISO-8859-1')
# predictions = model.predict(count_vectorizer.transform(df['Tweet']))

# submission = pd.DataFrame({'Id':df['Id'],'Type':predictions})
# submission['Type'] = submission['Type'].map({0:'Quality', 1:'Spam'})

# filename = 'predictions.csv'
# submission.to_csv(filename,index=False)
