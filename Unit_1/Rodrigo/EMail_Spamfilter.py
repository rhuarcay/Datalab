# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 08:27:28 2020

@author: Rodrigo
"""
emails=[]
labels=[]
namen=[]
email_text=[]
text = ""
P = []

import numpy as np
import email as ml
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

def Import_Data():
    import zipfile as zipp
    z = zipp.ZipFile('Spam_Data_Mail.zip')
    
    names = z.namelist()
    names = names[1:]
    print(names[0])
    
    for name in names:
        email = z.read(name)
        emails.append(email)
    for name in names:
        tok = name.split('/')
        labels.append(tok[0])
    for name in names:
        tok = name.split('/')
        namen.append(tok[1])
    for email in emails:
        global text
        text=""
        message = ml.message_from_bytes(email)
        extrakt_payload(message)
        email_text.append(text)

def extrakt_payload(message):
    global text
    if message.is_multipart():
        for payload in message.get_payload():
            extrakt_payload(payload)
    else:
        text = text + " " + message.get_payload()  

def Model_ohne_Norm_Optimierung():
    cv = CountVectorizer(min_df = 0.001, max_df = 0.25)
    cv.fit(X_Train)
    
    x_Train = cv.transform(X_Train)
    x_Test = cv.transform(X_Test)
    y_Train = np.array(Y_Train)
    y_Test = np.array(Y_Test)
    
    print(x_Train.shape)
    print(x_Test.shape)
    
    print("The Model is been trained")
    model = SVC(C=1, kernel='rbf', gamma=1)
    model.fit(x_Train, y_Train)
    
    print(model.score(x_Test, y_Test))
    P = model.predict(x_Test)
    print(np.mean(P == y_Test))  
    
def Model_mit_Norm_Optimierung():
    #Pipeline um mehrere möglichkeiten zu probieren
    pipeline = Pipeline([
        ("cv", CountVectorizer()),
        ("tffidf", TfidfTransformer()),
        ("svm", SVC())    
    ])
    
    clf = GridSearchCV(pipeline, param_grid = {
        "svm__C": [0.01,0.1,1,10,100],
        "svm__gamma": [0.01,0.1,1,10,100],
       # "tffidf": [True,False],
       #"cv__max_df": [0.25,0.5, 0.75, 1.0],
       #"cv__min_df": [0.0001,0.001,0.01,0.1]
    })
    
    print("Model is being trained")
    clf.fit(X_Train, Y_Train)
    
    print(clf.best_params_)
    print(clf.score(X_Test,Y_Test))
    global P
    P = clf.predict(X_Test)
    print(np.mean(P==Y_Test))
    print("......The Model is trained.....")

Import_Data()

X_Train, X_Test, Y_Train, Y_Test = train_test_split(email_text,labels, random_state=0)

Model_mit_Norm_Optimierung()
      
        