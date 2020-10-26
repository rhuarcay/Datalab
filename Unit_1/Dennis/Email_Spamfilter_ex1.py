# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 11:06:59 2020

@author: Dennis
"""

import numpy as np
import zipfile as zipp

import sklearn.svm as svm

emails = []
labels = []

#Das hier könnte theoretisch als Importfunktioniert definiert werden

z = zipp.ZipFile('../Data/882c3758e63a664bed3dfceb44f60c96363572c8.zip')

names = z.namelist()

for name in names[:-1]:
    email = z.read(name)
    emails.append(email)
    
for name in names[:-1]:
    tok = name.split('.')
    labels.append(int(tok[1]))
    
#-------------------------------------------------------------
    

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

print(classifier.score(Xts, Yts))