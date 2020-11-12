# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:35:43 2020

@author: guine
"""
FILE = '../Data/Data_Ex1.zip'

import numpy as np
import zipfile as zipp
import sklearn.svm as svm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

#Gib ne file rein, die features werden extrahiert und als features und labels
#wieder ausgegeben
#Eventuell könnt man noch die Dateinamen dabei zurückgeben, für später... mal schauen.
def prepare_data(file):
    namelist = []
    text = []
    
    namelist, labellist = extrakt_Names(file)
    text = extrakt_Tree(namelist)
    
    print("Features werden extrahiert, bitte warten...")
    vbaList = feature_vbaProject(text)
    picList = feature_pictures(text)
    picCount = feature_pictures(text, count=True)
    badzip = feature_badzipfile(text)
    olelist = feature_ole(text)
    print("Features extrahiert!")
    
    features = np.zeros((len(text), 5))
    
    for i in range(0, len(text)):
        features[i,0]=vbaList[i]
        features[i,1]=picList[i]
        features[i,2]=picCount[i]
        features[i,3]=badzip[i]
        features[i,4]=olelist[i]
    
    labels = np.array(labellist)
    
    return features, labels


#Gibt die Namen der Dateien und die Label dazu zurück
def extrakt_Names(file):
    zf = zipp.ZipFile(file)
    name = zf.namelist()
    name = name[:-1]
    labels = extrakt_Labels(name)
    return name, labels

#Erwartet eine Liste an Dateinamen, und extrahiert daraus das Label.
#Nur für das Training relevant
def extrakt_Labels(nameList):
    labels_i=[]
    for name in nameList:
        tok = name.split('.')
        labels_i.append(int(tok[1]))
    return labels_i

#Extrahiert die Namen aller Dateien aus den Docx-Dateien
def extrakt_Tree(nameList):
    features_tree=[]
    for names in nameList:
        tree=[]
        try:
            f = zipp.ZipFile('../Data/Data_Ex1/'+names)
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

#Verarbeitet die Liste von Listen von Dateien zu einer Liste an Strings
#Die Dateinamen werden dabei einfach nacheinander in einen String gespeichert
#Und in eine Liste geworfen
def listlist_to_stringlist(l):
    stringlist = []
    for entry in l:
        string = ''
        for list_entry in entry:
            string = string + ' ' + list_entry
        stringlist.append(string)
    return stringlist

#Verarbeitet die Liste von Listen von Dateien zu einer Liste an überhaupt existierenden files
#Praktisch für das Extrahieren von features. Maybe.
def get_filenames(l):
    string_list = []
    for entry in l:
        for list_entry in entry:
            if (not(list_entry in string_list)):
                string_list.append(list_entry)
    string_list.sort()
    return string_list

#Erwartet als Input eine Liste an Liste von Dateien aus den Docx-Dateien.
#Dabei wird gezählt, welche Dateinamen wie oft in den Dokumenten vorkommen
#Rückgabe ist ein Dictionray, wobei die keys die Filenamen und die Values
#die Anzahl der Files sind
def count_filenames(featurelist):
    file_dict = {}
    filelist = get_filenames(featurelist)
    
    for file in filelist:
        file_dict[file] = 0
    
    for entry in featurelist:
        for list_entry in entry:
            file_dict[list_entry] = file_dict[list_entry]+1
            
    return file_dict

#Erwartet als Input eine Liste an Liste von Dateien aus den Docx-Dateien.
#Rückgabe ist eine Liste, ob die Datei  'vbaProject.bin' in der Liste ist
#oder nicht. (1 oder 0)
def feature_vbaProject(filelist):
    featurelist = []
    for l in filelist:
        if 'vbaProject.bin' in l:
            featurelist.append(1)
        else:
            featurelist.append(0)
    return featurelist

#Erwartet als Input eine Liste an Listen von Dateien aus den Docx-Dateien.
#Rückgabe ist eine Liste, ob Mediendateien vorhanden sind. (1 oder 0)
#Bei count = True wird stattdessen die Anzahl an vorhandenen Bildern zurückgegeben.
def feature_pictures(filelist, count = False):
    featurelist = []
    pic_ends = ['png', 'gif', 'jpg', 'jpeg', 'wdp', 'emf', 'wmf', 'JPG', 'PNG', 'EMF', 'jpe']
    for l in filelist:
        pic_exists = 0
        for name in l:
            tok = name.split('.')
            if tok[-1] in pic_ends:
                if not count:
                    pic_exists = 1
                else:
                    pic_exists = pic_exists + 1
        featurelist.append(pic_exists)
    return featurelist

#Erwartet als Input eine Liste an Listen von Dateien aus den Docx-Dateien
#Rückgabe ist eine Liste, ob die ursprüngliche Datei eine nichtlesbare Zipfile war oder nicht
def feature_badzipfile(filelist):
    featurelist = []
    for l in filelist:
        if 'BadZipfile' in l:
            featurelist.append(1)
        else:
            featurelist.append(0)
    return featurelist

#Erwartet als Input eine Liste an Listen von Dateien aus den Docx-Dateien
#Rückgabe ist eine Liste, ob in den Dateien eine ole-Datei vorhanden ist. Hoffentlich.
def feature_ole(filelist):
    featurelist = []
    for l in filelist:
        ole = 0
        for entry in l:
            if 'ole' in entry.lower():
                ole = 1
        featurelist.append(ole)
    return featurelist


def train_classifier(features, labels, pipe=False):
    
    X_train, X_test, Y_train, Y_test = train_test_split(features, labels, random_state=0)

    if pipe: 
        pipeline = Pipeline([
            ("tffidf", TfidfTransformer()),
            ("svm", svm.SVC())
        ])
        classifier = GridSearchCV(pipeline, param_grid = {
            "svm__C": [0.01, 0.1, 1, 10, 100, 1000],
            "svm__gamma": [0.01, 0.1, 1, 10, 100, 1000],
            "svm__kernel": ['rbf']
        })
    else:
        classifier = svm.SVC(C=1, kernel='rbf', gamma=1)
        
    print("Trainiere classifier")
    classifier.fit(X_train, Y_train)
    
    print('Classifier trainiert!')
    
    Y_pred = classifier.predict(X_test)
    print('Score:')
    print(balanced_accuracy_score(Y_test, Y_pred))
    if pipe:
        print("Best parameters:")
        print(classifier.best_params_)
    
    return classifier


#-------------------------------------------------

###
# namelist = []
# text = []

# namelist, labellist = extrakt_Names(FILE)
# text = extrakt_Tree(namelist)

# vbaList = feature_vbaProject(text)
# picList = feature_pictures(text)
# picCount = feature_pictures(text, count=True)
# badzip = feature_badzipfile(text)
# olelist = feature_ole(text)
###
X, Y = prepare_data(FILE)
c = train_classifier(X, Y, True)

#textlist = get_filenames(text)
#file_dict = count_filenames(text)

#textlist = listlist_to_stringlist(text)
#cv = CountVectorizer(encoding='utf-32')
#cv.fit(textlist)
