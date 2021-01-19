# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 13:23:54 2021

@author: Rodrigo
"""
import os
import numpy as np
import zipfile as zipp
import pickle
import re
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest
from sklearn import preprocessing
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import CountVectorizer



def write_In_file(in_file):
    """Writes a List to an outfile in the current directory"""
    name = in_file
    with open(in_file, "rb") as in_file:    
        in_list = pickle.load(in_file)
    
    return in_list

def write_to_output(outlier_tcpstream):
    f = open("outliers_model.txt", "wt")
    
    for tcp_stream in outlier_tcpstream:
        f.write("%s" % tcp_stream + '\n')
    
    f.close()

delimeter = "/","_", " ", "-", ",", ".", "\\"
regexPattern = '|'.join(map(re.escape, delimeter))
def my_tokenizer(text):
    """Custom Token erzeugung bei Text für CV"""
    return re.split(regexPattern, text)

def use_count_vectorizer(x_Data):
    
    cv = CountVectorizer(min_df = 0.001, max_df = 0.25, token_pattern=regexPattern)
    cv.fit(x_Data)
    
    cv_features = cv.transform(x_Data)
    
    return cv_features

def normalise_features(features):
    """Normalisierung der Features"""
    #features = Normalizer().fit_transform(features)
    features = StandardScaler().fit_transform(features) 
    return features

def manuel_outlier_detec(features):
    """Test Methode zur Filterung von Packets"""
    outliers=[]
    
    for counter, pkt in enumerate(features):
        if pkt[3] > 150:
            outliers.append(pkt)
    
    return outliers

def outlier_detec():
    """Erzeugung ein Outlier Detedtion Model"""
    #fit model
    clf = LocalOutlierFactor()
    #clf = OneClassSVM(kernel='rbf', gamma=0.1, verbose=True, nu=0.1)
    return clf

def outlier_entfernung(klassification, tcp_stream_index):
    """Erstellung ein Set mir alle Outlier"""
    pkt_set = {0}
    for counter, pkt in enumerate(klassification):
        if pkt == -1:
            pkt_set.add(counter)
    outlier_tcpstream = {0}
    for pkt in pkt_set:
        outlier_tcpstream.add(tcp_stream_index[pkt])
    return outlier_tcpstream

'''
def main():
    #For Trainings Daten
    total_features = write_In_file("Features.txt") #Features in List
    tcp_stream_index = total_features[:137952,0] #Index of Stream TCP + Src.ip etc
    features = total_features[:137952,3:8]
    
    features = normalise_features(features)
    clf = outlier_detec()
    klassification = clf.fit_predict(features)
    
    #-----
    
    
    
    
    return 0

if __name__ == "__main__":
    main()
'''
# NUR FÜR TESTING SONST IN MAIN
#For Trainings Daten
print("Importing Files")
total_features = write_In_file("Features.txt") #Features in List
tcp_stream_index = total_features[:137952,0] #Index of Stream TCP + Src.ip etc
#features = total_features[:137952,5:6] #Bytes
features = total_features[:137952,5:7] #Index
#features = np.concatenate((features,features2),axis = 1)
#manuel_out = manuel_outlier_detec(total_features[:137952,0:7])
Communikation = write_In_file("TCP_Verbindung.txt")
total_features2 = write_In_file("Features2.txt")
"""

print("Erzeugung CV Features")
x_Data = total_features[:137952, 2:3]
string_features = use_count_vectorizer(x_Data)


print("Normierung")
features = normalise_features(features)
clf = outlier_detec()
print("Outlier detection")
klassification = clf.fit_predict(features)
print("Erkennung von TCP_Stream")
outlier_tcpstream = outlier_entfernung(klassification, tcp_stream_index)
print("Writing a file out")
write_to_output(sorted(outlier_tcpstream))
"""