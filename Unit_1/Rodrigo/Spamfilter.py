# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:12:44 2020

@author: Rodrigo
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv(r'C:\Users\Rodrigo\Desktop\TU-Braunschweig\WS20-21\Datalab\Unit_1\Test_Spam_Filter\spam.csv')

#print (len(df))

X = df["message"]
Y = df["type"]

X_Train, X_Test, Y_Train, Y_Test = train_test_split(X,Y, random_state=0)

cv = CountVectorizer(min_df = 0.001, max_df = 0.25)
cv.fit(X_Train)

X_Train = cv.transform(X_Train)
X_Test = cv.transform(X_Test)
Y_Train = np.array(Y_Train)
Y_Test = np.array(Y_Test)

print(X_Train.shape)
print(X_Test.shape)

model = MultinomialNB()
model.fit(X_Train, Y_Train)

print(model.score(X_Test, Y_Test))
