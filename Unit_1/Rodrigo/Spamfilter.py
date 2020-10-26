# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:12:44 2020

@author: Rodrigo
"""
emails=[]
labels=[]
namen=[]
email_text=[]
text = ""
P = []

import pandas as pd
import email as ml
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.naive_bayes import MultinomialNB


def extrakt_payload(message):
    global text
    if message.is_multipart():
        for payload in message.get_payload():
            extrakt_payload(payload)
    else:
        text = text + " " + message.get_payload()


import zipfile as zipp
z = zipp.ZipFile('../Data/882c3758e63a664bed3dfceb44f60c96363572c8.zip')

names = z.namelist()
#names = names[1:]
print(names[0])
   

for name in names[:-1]:
    email = z.read(name)
    emails.append(email)
for name in names[:-1]:
    tok = name.split('.')
    labels.append(tok[1])
for name in names[:-1]:
    tok = name.split('.')
    namen.append(tok[0])
for email in emails:
    text=""
    message = ml.message_from_bytes(email)
    extrakt_payload(message)
    email_text.append(text)



X_Train, X_Test, Y_Train, Y_Test = train_test_split(email_text,labels, random_state=0)

cv = CountVectorizer(min_df = 0.001, max_df = 0.25)
cv.fit(X_Train)

X_Train = cv.transform(X_Train)
X_Test = cv.transform(X_Test)
Y_Train = np.array(Y_Train)
Y_Test = np.array(Y_Test)

print(X_Train.shape)
print(X_Test.shape)

print("Model wird trainiert")
model = MultinomialNB()
model.fit(X_Train, Y_Train)

print(model.score(X_Test, Y_Test))
