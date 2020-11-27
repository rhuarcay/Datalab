# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:35:43 2020

@author: guine
"""
FILE = '../Data/Data_Ex1'
TESTFILE = '../Data/Testdata_Ex1'

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
def prepare_trainingsdata(file):
    namelist = []
    text = []
    
    namelist= extract_Names(file)
    namelist = namelist[:-1]        #weil das hier die Labeldatei ist
    labellist = extract_Labels(namelist)
    text = extract_Tree(namelist, file)
    
    features = extract_features(text)
    
    labels = np.array(labellist)
    
    return features, labels


#Gibt die Namen der Dateien und die Label dazu zurück
def extract_Names(file):
    file = file + '.zip'
    zf = zipp.ZipFile(file)
    name = zf.namelist()
    return name

#Erwartet eine Liste an Dateinamen, und extrahiert daraus das Label.
#Nur für das Training relevant
def extract_Labels(nameList):
    labels_i=[]
    for name in nameList:
        tok = name.split('.')
        labels_i.append(int(tok[1]))
    return labels_i

def extract_features(data):
    print("Features werden extrahiert, bitte warten...")
    vbaList = feature_vbaProject(data)
    picList = feature_pictures(data)
    picCount = feature_pictures(data, count=True)
    badzip = feature_badzipfile(data)
    olelist = feature_ole(data)
    print("Features extrahiert!")
    
    features = np.zeros((len(data), 5))
    
    for i in range(0, len(data)):
        features[i,0]=vbaList[i]
        features[i,1]=picList[i]
        features[i,2]=picCount[i]
        features[i,3]=badzip[i]
        features[i,4]=olelist[i]

    return features

#Extrahiert die Namen aller Dateien aus den Docx-Dateien
def extract_Tree(nameList, path):
    features_tree=[]
    for names in nameList:
        tree=[]
        try:
            f = zipp.ZipFile(path + '/' + names)
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
        except:
            print('Bad: ' + path + '/' + names)
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


def train_classifier(features, labels, pipe=False, all_data=False):
    
    if all_data:
        X_train = features
        Y_train = labels
        classifier = svm.SVC(C=1, kernel='rbf', gamma=1) 
    else:
        X_train, X_test, Y_train, Y_test = train_test_split(features, labels, random_state=0)
        if pipe: 
            pipeline = Pipeline([
                #("tffidf", TfidfTransformer()),
                ("svm", svm.SVC())
            ])
            classifier = GridSearchCV(pipeline, param_grid = {
                "svm__C": [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000],
                "svm__gamma": [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000],
                "svm__kernel": ['rbf']
            })
        else:
            classifier = svm.SVC(C=1, kernel='rbf', gamma=1)
        
    print("Trainiere classifier")
    
    classifier.fit(X_train, Y_train)
    
    print('Classifier trainiert!')
    
    if (not all_data):
        Y_pred = classifier.predict(X_test)
        print('Score:')
        print(balanced_accuracy_score(Y_test, Y_pred))
        if pipe:
            print("Best parameters:")
            print(classifier.best_params_)
    
    return classifier



def classify_data(file, modelfile):
    names = extract_Names(file)
    text = extract_Tree(names, file)
    X = extract_features(text)
    #Features normalisieren!!!
    try:
        classifier = load_model(modelfile)
    except:
        print("Model falsch oder nicht vorhanden")
        return (names, X, False)
    
    try:
        print('Starte Klassifizierung')
        Y = classifier.predict(X)
        print('Klassifizierung abgeschlossen')
        #Ev Y und names zusammenschmeißen als ein Array.
        #Das zurückgeben, mit true, weil hat funktioniert
        Z = []
        return (names, Y, True)
    except:
        print('Klassifierung fehlgeschlagen. Möglicherweise wurde ein falsches Modell genutzt?')
        return (names, Y, False)



def write_to_file(names, label):
    f = open("docx-test.predict", "wt")
    
    for name, pred in zip(names, label):
        f.write("%s;%d" % (name, pred) + '\n')
    
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


#Das hier ist so der Teil zum Trainieren
#X, Y = prepare_trainingsdata(FILE)
#c = train_classifier(X, Y, pipe=False, all_data=True)
#save_model(c, 'classifier_docx')

x = classify_data(TESTFILE, 'classifier_docx.joblib')
if (x[2]):
    write_to_file(x[0], x[1])
#Hier der Teil zum Klassifizieren



