# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:35:41 2020

@author: Rodrigo
"""
FILE = 'Data_Ex1.zip'

import zipfile as zipp
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

def extrakt_Names(file):
    zf = zipp.ZipFile(file)
    name = zf.namelist()
    name = name[:-1]
    labels = extrakt_Labels(name)
    return name, labels

def extrakt_Labels(nameList):
    labels_i=[]
    for name in nameList:
        tok = name.split('.')
        labels_i.append(int(tok[1]))
    return labels_i



def extrakt_Tree(nameList):
    features_tree=[]
    for names in nameList:
        tree=[]
        try:
            f = zipp.ZipFile(names)
            wordFile = f.namelist()
            for structure in wordFile[1:]:
                tok = structure.split('/')
                txt = ""
                tree.append(txt.join(tok[1:]))
            features_tree.append(tree)
        except zipp.BadZipFile:
            tree.append("BadZipfile")
            features_tree.append(tree)
            continue
    return features_tree

def count_vectorizer_SVM(x_Data, y_Data):
    
    X_train, X_test, Y_train, Y_test = train_test_split(x_Data, y_Data, random_state=0)
    
    #cv = CountVectorizer(min_df = 0.001, max_df = 0.25)
    #cv.fit(X_train)
    
    #x_train = cv.transform(X_train)
    #x_test = cv.transform(X_test)
    #y_train = np.array(Y_train)
    #y_test = np.array(Y_test)
    
    #Pipeline um mehrere möglichkeiten zu probieren
    pipeline = Pipeline([
        ("cv", CountVectorizer()),
        ("tffidf", TfidfTransformer()),
        ("svm", SVC())    
    ])

    clf = GridSearchCV(pipeline, param_grid = {
        "svm__C": [1],
        "svm__gamma": [1],
       #"tffidf": [True,False],
       #"cv__max_df": [0.25,0.5, 0.75, 1.0],
       #"cv__min_df": [0.0001,0.001,0.01,0.1]
    })
    
    print('Trainiere Classifier, bitte warten...')
    
    #Nur mit 0.75 der Daten trainiert! Fürs real mit 100% Trainieren
    clf.fit(X_train, Y_train)
    
    print('Classifier trainiert!')
      
    y_pred = clf.predict(X_test)
    
    print('Score:')
    print(clf.score(X_test, Y_test))
    print(balanced_accuracy_score(Y_test, y_pred))
    print(np.mean(y_pred==Y_test))
    return clf

def listlist_to_stringlist(l):
    stringlist = []
    for entry in l:
        string = ''
        for list_entry in entry:
            string = string + ' ' + list_entry
        stringlist.append(string)
    return stringlist

#-------------------------------------------------
namelist = []
text = []
labels =[]

namelist, labels = extrakt_Names(FILE)
text = extrakt_Tree(namelist)
textlist = listlist_to_stringlist(text)
classifier = count_vectorizer_SVM(textlist, labels)
