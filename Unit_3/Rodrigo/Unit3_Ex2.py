# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:11:58 2020

@author: Rodrigo&Dennis
"""

from androguard import misc
from androguard import session
import os
import numpy as np
import zipfile as zipp
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

MY_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = '../Data/Data_Ex2'
FILE_VM = 'Data_Ex2'
TESTFILE = '../Data/Testdata_Ex2'


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

def write_Out_file(out_filename, out_list):
    """ Writes a List in a Outfile in the current directory
        used to store for Exam. the Permissions"""    
    
    with open(out_filename, "wb") as out_file:
        pickle.dump(out_list, out_file)

def write_In_file(in_file):
    """Writes a List to an outfile in the current directory"""
    name = in_file
    with open(in_file, "rb") as in_file:    
        in_list = pickle.load(in_file)
    
    out_list = []
    #if Permission gibt only the Permissiom
    if name == "Permissions_Data.txt" or name == "Activity_Data.txt" or name == "Permissions_Testdata.txt":
        for list in in_list:
            out_list_2=[] 
            for string in list:
                s = string.split(".")[-1]
                out_list_2.append(s)
            out_list.append(out_list_2)
    else:
        out_list = in_list
            
    return out_list

def listlist_to_stringlist(l):
    """ Verarbeitet die Liste von Listen von Dateien zu einer Liste an Strings
        Die Dateinamen werden dabei einfach nacheinander in einen String gespeichert
        Und in eine Liste geworfen"""
    stringlist = []
    for entry in l:
        string = ''
        for list_entry in entry:
            string = string + ' ' + list_entry
        stringlist.append(string)
    return stringlist

def extract_Permissions(name_list):
    """Function takes the permissions from a Apk File and stores it in a list"""
    permissions = []
    
    print("Permissions werden extrahiert, bitte warten...")
    print("0/1000")
    i = 0 
    
    for file in name_list:
        
        # get a default session
        sess = misc.get_default_session()
        try:
            a, d, dx = misc.AnalyzeAPK(file) # APK return 3 Elements a ist the 
        
            #permissions.append(a.get_permissions())
            permissions.append(a.get_activities())
            sess.reset()
        except:
            permissions.append("Activities couldnt be extracted")
            print("error in Activities")
            sess.reset()
        
        i+=1
        print(str(i)+"/1000 has been processed")
        
        
    print("Permissions already processed")
    print("Saving Permissions...")
    
    #permissions = listlist_to_stringlist(permissions)
    write_Out_file("Activities.txt", permissions)    
    
    return permissions


def load_model(filepath):
    from joblib import load
    model = load(filepath)
    print('Model geladen von ' + filepath)
    return model

def clustering_kMeans(permissions_list, labels_list):
    """ This Functions gets a list of Permissions and use the Kmeans Cluster with the
        the elbow method"""
    labels_list = np.array(labels_list)
    inertia = [1]
    labels_predicted = []
    for n in range(1,25):
        pipeline = Pipeline([
            ("cv", CountVectorizer(min_df=0.15)),
            ("tffidf", TfidfTransformer()),
            #("scaler", StandardScaler()),
            ("cluster", KMeans(n_clusters = n) )
            ])
        
        labels_predicted = pipeline.fit_predict(permissions_list)
        inertia.append(pipeline.named_steps['cluster'].inertia_)
        #silhouette = silhouette_score(labels_list,labels_predicted)
        silhouette = ""
        score = adjusted_rand_score(labels_predicted, labels_list)
        print("Score for " + str(n) + " Clust: " + str(score)[:6]+ "/ Inertia: " +
              str(inertia[n])[:6]+ "/ % " + str(((inertia[n]-inertia[n-1])/inertia[n-1])*100))
    
    
    return labels_predicted


def clustering_KMeans_Testdata(features):
    """ This Functions gets a list of Permissions and use the Kmeans Cluster with the
        the elbow method"""
    inertia = [1]
    labels_predicted = []
    for n in range(1,25):
        pipeline = Pipeline([
            ("cv", CountVectorizer(min_df=0.15)),
            ("tffidf", TfidfTransformer()),
            #("scaler", StandardScaler()),
            ("cluster", KMeans(n_clusters = n) )
            ])
        
        labels_predicted = pipeline.fit_predict(features)
        inertia.append(pipeline.named_steps['cluster'].inertia_)
        print("Score for " + str(n) + " Clust: / Inertia: " + str(inertia[n])[:6]+ "/ % " + str(((inertia[n]-inertia[n-1])/inertia[n-1])*100))       
    
    return 0
    
def main():
    
    name_list = extract_Names(TESTFILE)
    #labels_list = extract_Labels(name_list)
    #permissions = extract_Permissions(name_list)
    
    """
    permissions = write_In_file("Permissions_Data.txt")
    permissions = listlist_to_stringlist(permissions)
    
    activities = write_In_file("Activity_Data.txt")
    activities = listlist_to_stringlist(activities)
    
    provider = write_In_file("Provider_Data.txt")
    provider = listlist_to_stringlist(provider)
    for i, file in enumerate(provider):
        provider[i] = provider[i].split(".")
    provider = listlist_to_stringlist(provider)
    
    receiver = write_In_file("Receiver_Data.txt")
    receiver = listlist_to_stringlist(receiver)
    for i, file in enumerate(receiver):
        receiver[i] = receiver[i].split(".")
    receiver = listlist_to_stringlist(receiver)
    
    service = write_In_file("Service_Data.txt")
    service = listlist_to_stringlist(service)
    for i, file in enumerate(service):
        service[i] = service[i].split(".")
    service = listlist_to_stringlist(service)
    """
    permissions_test = write_In_file("Permissions_Testdata.txt")
    permissions_test = listlist_to_stringlist(permissions_test)
    
    #Merging the 5 Lists together
    #features = [a for a,b,c,d,e in zip(permissions, activities, provider, receiver, service)]
    
    #features = write_In_file("FEATURES.txt")
    
    #labels_predicted = clustering_kMeans(features, labels_list)
    clustering_KMeans_Testdata(permissions_test)
    
    return 0



if __name__ == "__main__":
    main()