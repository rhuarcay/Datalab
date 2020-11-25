# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 11:51:39 2020

@author: Rodrigo
"""
import zipfile as zipp
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift

MY_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = '../Data/Data_Ex1'
TESTFILE = 'Testdata_Ex1'

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

def extract_text_php(file):
    """Function to extract the Text from the Php Files"""
    file = file + '.zip'
    with zipp.ZipFile(file) as zfile:
        docs = list(map(lambda name: zfile.read(name).decode("latin1"), zfile.namelist()[:-1]))
    
    return docs

def clustering_kMeans(text_list, label_list):
    """Clustering the Text with CV with kMeans"""
    #for n in range(3,7):
    print('Data is been clustered... ')
    pipeline = Pipeline([
        ("cv", CountVectorizer(strip_accents='ascii',min_df=0.25)),
        ("tffidf", TfidfTransformer()),
        ("cluster", MeanShift() )
        ])
    
    labels_predicted = pipeline.fit_predict(text_list)
    score = adjusted_rand_score(labels_predicted, label_list)
    print("Score for " + str(2) + " Clusters: " + str(score))

def main():
    
    name_list = extract_Names(FILE)
    labels = extract_Labels(name_list)
    text_docs = extract_text_php(FILE)
    
    clustering_kMeans(text_docs, labels)
    
    return 0

if __name__ == "__main__":
    main()