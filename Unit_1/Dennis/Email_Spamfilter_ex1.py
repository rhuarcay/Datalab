# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 11:06:59 2020

@author: Dennis
"""

import numpy as np
import zipfile as zipp

import sklearn.svm as svm
import email as ml
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import balanced_accuracy_score


def Import(datapath):
    if (type(datapath) != str):
        print('Wrong input')
        return
        
    #z = zipp.ZipFile('../Data/882c3758e63a664bed3dfceb44f60c96363572c8.zip')
    z = zipp.ZipFile(datapath)
    
    emails = []
    labels = []
    emails_text = []
    
    names = z.namelist()
    
    for name in names[:-1]:
        email = z.read(name)
        emails.append(email)
        
    for name in names[:-1]:
        tok = name.split('.')
        labels.append(int(tok[1]))
        
    for email in emails:
        global text
        text=""
        message = ml.message_from_bytes(email)
        extract_payload(message)
        emails_text.append(text)
        
    return emails, labels, emails_text
    
#-------------------------------------------------------------

def extract_payload(message):
    global text
    if message.is_multipart():
        for payload in message.get_payload():
            extract_payload(payload)
    else:
        text = text + " " + message.get_payload() 

#Dieser Classifier arbeitet nur mit einem Feature: der Länge der Email
#Don't use that. Das war nur ein grundlegender Test
def bad_classifier(data):
    emails, labels, emails_text = Import(data)
    
    X = np.zeros((len(emails),1))
    
    Y = np.array(labels)
    
    for i, email in enumerate(emails):
        X[i] = len(email)
        
    idx = np.random.permutation(16662)    
    
    Xtr = X[idx[:8000],:]
    Xts = X[idx[8000:],:]
    
    Ytr = Y[idx[:8000]]
    Yts = Y[idx[8000:]]    
    
    classifier = svm.SVC(C=100, kernel='rbf')
    
    classifier.fit(Xtr, Ytr)
    
    Ypred = classifier.predict(Xts)
    print('Score:')
    print(balanced_accuracy_score(Yts, Ypred))
    
    return classifier
    
    
def classifier_count(datapath):
    emails, labels, emails_text = Import(datapath)
    
    X_train, X_test, Y_train, Y_test = train_test_split(emails_text, labels, random_state=0)
    
    cv = CountVectorizer(encoding='utf-32', min_df = 0.001, max_df = 0.25)
    cv.fit(X_train)
    
    x_train = cv.transform(X_train)
    x_test = cv.transform(X_test)
    y_train = np.array(Y_train)
    y_test = np.array(Y_test)
    
    print('Trainiere Classifier, bitte warten...')
    
    classifier = svm.SVC(C=1, kernel='rbf', gamma=1)
    classifier.fit(x_train, y_train)
    
    print('Classifier trainiert!')
    
    y_pred = classifier.predict(x_test)
    print('Score:')
    print(balanced_accuracy_score(y_test, y_pred))
    
    return cv, classifier
    

def classify_count(datapath, cv, classifier):
    emails, labels, emails_text = Import(datapath)
    
    email_features = cv.transform(emails_text)
    
    P = classifier.predict(email_features)
    
    return P

def write_to_file(names, label):
    f = open("spam1-test.predict", "wt")
    
    for name, pred in zip(names, label):
        f.write("%s;%d" % (name, pred))
    
    f.close()
    
#--------------------------------------------------------------------------------
#Hier die Funktionen für das Speichern und Laden eines Models:

#model: Das Model, was gespeichert werden soll - sei es ein Tupel oder einfach nur der Classifier
#filename: Name der file, in dem das landen soll. In der Funktion wird noch die Dateiendung gesetzt, wird hier nicht benötigt
def save_model(model, filename):
    from joblib import dump
    name = filename + '.joblib'
    dump(model, name)
    print('Model gespeichert unter ' + name)
    
#filepath: Pfad zu der Datei, die geladen werden soll. (Oder nur der Dateiname, wenn die Datei direkt da ist)
#TODO: noch überprüfen, obs ne .joblib-Datei ist.
def load_model(filepath):
    from joblib import load
    model = load(filepath)
    print('Model geladen von ' + filepath)
    return model
#--------------------------------------------------------------------------------
    

#P = bad_classifier('../Data/Data_Ex1.zip')
emails,labels,emails_text = Import('../Data/Data_Ex2.zip')


#cv, classifier = classifier_count('../Data/882c3758e63a664bed3dfceb44f60c96363572c8.zip')
#P = classify_count('../Data/882c3758e63a664bed3dfceb44f60c96363572c8.zip', cv, classifier)