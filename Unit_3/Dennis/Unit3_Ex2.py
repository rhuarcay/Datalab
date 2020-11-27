# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:34:53 2020

@author: guine
"""
import numpy as np
import zipfile as zipp
import pickle

from androguard import misc
from androguard import session

from sklearn.cluster import MeanShift
from sklearn.metrics import adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

FILE = '../Data/Data_android'


def extract_Names(file):
    """Gibt die Namen der Dateien und die Label dazu zurück"""
    file = file + '.zip'
    zf = zipp.ZipFile(file)
    name = zf.namelist()[:-1]
    return name


def extract_Labels(nameList):
    """ Erwartet eine Liste an Dateinamen, und extrahiert daraus das Label.
        Nur für das Training relevant"""
    labels_i=[]
    for name in nameList:
        tok = name.split('.')
        labels_i.append(int(tok[1]))
    return labels_i

def extract_all_permissions(name_list):
    permissions = set()
    
    for file in name_list:
        
        # get a default session
        sess = misc.get_default_session()
        try:
            a, d, dx = misc.AnalyzeAPK('../Data/Data_android/' + file) # APK return 3 Elements a ist the 
            
            for perm in a.get_permissions():
                permissions.add(perm)
            sess.reset()
        except:
            permissions.add("Permission_error")
            print("error in Permissions")
            sess.reset()
    
    return permissions


def create_permission_dict(permission_set):
    per_dict = {}
    for permission in permission_set:
        per_dict[permission] = 0
    return per_dict

def reset_dict(per_dict):
    for key in per_dict.keys():
        per_dict[key] = 0
    return per_dict

def extract_permission_features(name_list, permission_set):
    #TAnzahl an permissions herausfinden!
    per = len(permission_set)
    #Anzahl an APK's herausfinden!
    apk = len(name_list)
    
    #Numpy-Array der richtigen Größe anlegen
    features = np.zeros((apk, per))
    
    per_dict_list = []
    
    print("Permissions werden extrahiert, bitte warten...")
    print("0/" + str(apk))
    i = 0 
    
    for file in name_list:
        per_dict = create_permission_dict(permission_set)
        
        sess = misc.get_default_session()
        try:
            a, d, dx = misc.AnalyzeAPK('../Data/Data_android/' + file) # APK return 3 Elements a ist the 
        
            for perm in a.get_permissions():
                per_dict[perm] = 1
        except:
            per_dict["Permission_error"] = 1
        
        sess.reset()
        per_dict_list.append(per_dict)
        i+=1
        print(str(i)+"/"+ str(apk) + " has been processed")
    
    print("Permissions processed")
    print("Featurevektoren werden erstellt...")
    
    for c, key in enumerate(permission_set):
        for i in range(apk): #Range von der Anzahl an APK's
            features[i][c] = per_dict_list[i][key]
            #!!!Aufpassen!!! Index in np-arrays startet bei 0!
            
    print("Featurevektoren wurden erstellt!")
    
    return features

def cluster_meanshift(features, labels):
    #classifier = MeanShift(bandwidth = 2, cluster_all=False)
    #classifier.fit(features)
    
    #score = adjusted_rand_score(classifier.labels_, labels)
    #print("Score: " + str(score))
    
    
    
    pipeline = Pipeline([
        #("tffidf", TfidfTransformer()),
        ("cluster", MeanShift())
        ])
    classifier = GridSearchCV(pipeline, param_grid = {
        "cluster__bandwidth": [1, 1.5, 2, 2.5, 3],
        "cluster__min_bin_freq": [1, 2, 3, 4, 5],
        "cluster__max_iter": [200, 300, 400, 500, 750, 1000]
        }, scoring = 'adjusted_rand_score')
    
    print("Trainiere classifier")
    classifier.fit(features, labels)
    print('Classifier trainiert!')
    
    return classifier

def write_Out_file(out_filename, out):
    """ Writes a List in a Outfile in the current directory
        used to store for Exam. the Permissions"""    
    
    with open(out_filename, "wb") as out_file:
        pickle.dump(out, out_file)

def read_In_file(in_file):
    """Writes a List to an outfile in the current directory"""
    with open(in_file, "rb") as in_file:    
        in_list = pickle.load(in_file)
    
    return in_list

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
    
name_list = extract_Names(FILE)
labels_list = extract_Labels(name_list)
labels_array = np.array(labels_list)
    
#permissions = extract_all_permissions(name_list)
permissions = read_In_file('permission_set.pickle')

#features = extract_permission_features(name_list, permissions)
features = load_model('permission_features.joblib')

classifier = cluster_meanshift(features, labels_array)
print(np.unique(classifier.labels_))
