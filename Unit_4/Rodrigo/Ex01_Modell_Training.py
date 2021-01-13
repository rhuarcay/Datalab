# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 08:33:15 2020

@author: Rodrigo
"""

import os
import numpy as np
import zipfile as zipp
import pickle
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

def write_In_file(in_file):
    """Writes a List to an outfile in the current directory"""
    name = in_file
    with open(in_file, "rb") as in_file:    
        in_list = pickle.load(in_file)
    
    return in_list

def multiclass_SVM(features, labels):
    """
    Hier wird das Multiclas SVM trainiert
    Parameters
    ----------
    features : TYPE
        Features für das Trainieren des Modells.
    labels : TYPE
        Labeles.

    Returns
    -------
    clf : Gridsearch
        Trainiertes Modell.

    """
    
    features2 = features[:,:6]
    
    #Spliting the data 0,75
    X_train, X_test, Y_train, Y_test = train_test_split(features2, labels, random_state=0)
    # 100%
    X_train = features2
    Y_train = labels
    
    
    scaler = StandardScaler()
    scaler.fit(X_train)
    
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    
    #OneVSRest SVM
    #ovr_svm = OneVsRestClassifier(SVC())
    ovo_svm = OneVsOneClassifier(SVC())
    """
    #Piepeline 
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", OneVsRestClassifier(SVC(kernel='rbf')))
        ])
    """
    
    clf = GridSearchCV(ovo_svm, param_grid = {
        "estimator__kernel": ["rbf", "linear"],
        "estimator__C": [0.1, 1,10,100],
        "estimator__gamma": [0.1, 1,10,100]}, scoring="accuracy", verbose=1
        )
    
    
    print('Trainiere Classifier, with 100% of the Train Data, bitte warten...')
    clf.fit(X_train, Y_train)
    #print(clf.best_estimator_.)
    print('Classifier trainiert!')
    y_pred = clf.predict(X_test)
    
    print("Score: ")
    print(clf.score(X_test, Y_test))
    print(accuracy_score(Y_test, y_pred))
    
    return clf

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

def write_to_output(names, label):
    f = open("output.csv", "wt")
    
    for name, pred in zip(names, label):
        f.write("%s;%s" % (name, pred) + '\n')
    
    f.close()

def classify_data(features, test_features):
    
    features2 = features[:,:6]
    X_train = features2
    scaler = StandardScaler()
    scaler.fit(X_train)
    
    #scaled Test Features
    test_features2 = test_features[:,:6]
    s_Test_features = scaler.transform(test_features2)
    
    print("Loading Model...")
    clf = load_model("Multiclass_SVM.joblib") #Einlesen des trainierten Modells
    
    print("Starting to Classify...")
    predictions = clf.predict(s_Test_features)
    
    return predictions
    
def main():
        
    #For Trainingsdaten
    #------------------------------------------
    #features = write_In_file("Features.txt")
    #labels = write_In_file("Labels.txt")
    #Prepocesing von Labels
    #le = preprocessing.LabelEncoder()
    #le.fit(labels)
    #From Nominal to Ordinal Values
    #enc_labels = le.transform(labels)
    #clf = multiclass_SVM(features, enc_labels)
    #save_model(clf, "Multiclass_SVM")
    #----------------------------------------------------
    #For Testdaten
    
    #Einlesen der Features und Namen
    #test_features = write_In_file("TestData_Features.txt")
    #names = write_In_file("TestData_Labels.txt")
    
    #Predictions vom Model
    #predictions = classify_data(features, test_features)
    #str_predictions = le.inverse_transform(predictions)
    
    #write_to_output(names, str_predictions)
    
    print("Classifizierung Done....")
    
    return 0



if __name__ == "__main__":
    main()