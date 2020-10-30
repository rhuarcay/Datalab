# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 16:32:14 2020

@author: Rodrigo
"""
emails=[]
labels=[]
namen=[]
email_text=[]
text = ""


import numpy as np
import email as ml
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import zipfile as zipp

def extrakt_payload(message):
    global text
    if message.is_multipart():
        for payload in message.get_payload():
            extrakt_payload(payload)
    else:
        text = text + " " + message.get_payload()


z = zipp.ZipFile('C:/Users/Rodrigo/Desktop/TU-Braunschweig/WS20-21/Datalab/Unit_1/Trainingsdaten/U1_A1_Training.zip')

names = z.namelist()

for name in names[:-1]:
    email = z.read(name)
    emails.append(email)
for name in names[:-1]:
    tok = name.split('.')
    labels.append(int(tok[1]))
for name in names[:-1]:
    tok = name.split('.')
    namen.append(tok[0])
for email in emails:
    text=""
    message = ml.message_from_bytes(email)
    extrakt_payload(message)
    email_text.append(text)

X_Train, X_Test, Y_Train, Y_Test = train_test_split(email_text,labels, random_state=0)

#Pipeline um mehrere möglichkeiten zu probieren
pipeline = Pipeline([
    ("cv", CountVectorizer()),
    ("tffidf", TfidfTransformer()),
    ("svm", SVC())    
])

clf = GridSearchCV(pipeline, param_grid = {
    "svm__C": [1],
    "svm__gamma": [1],
   # "tffidf": [True,False],
   #"cv__max_df": [0.25,0.5, 0.75, 1.0],
   #"cv__min_df": [0.0001,0.001,0.01,0.1]
})

print("Model is being trained")
clf.fit(X_Train, Y_Train)

print(clf.best_params_)
print(clf.score(X_Test,Y_Test))

predicted_Train = clf.predict(X_Test)
print(np.mean(predicted_Train==Y_Test))
print("......The Model is trained.....")