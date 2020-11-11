# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:35:41 2020

@author: Rodrigo
"""
FILE = '../Data/Data_Ex1.zip'

import zipfile as zipp

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
        f = zipp.ZipFile('../Data/'+names)
        wordFile = f.namelist()
        for structure in wordFile[1:]:
            tok = structure.split('/')
            txt = ""
            tree.append(txt.join(tok[1:]))
        features_tree.append(tree)
    return features_tree

#-------------------------------------------------
namelist = []
text = []
labels =[]

namelist, labels = extrakt_Names(FILE)
text = extrakt_Tree(namelist)

'''In [39]: def extrakt_Tree(nameList):
    ...:     features_tree=[]
    ...:     for names in nameList:
    ...:         tree=[]
    ...:         try:
    ...:             f = zipp.ZipFile(names)
    ...:         except zipp.BadZipfile:
    ...:             tree.append("BadZipfile")
    ...:             features_tree.append(tree)
    ...:             continue
    ...:         wordFile = f.namelist()
    ...:         for structure in wordFile[1:]:
    ...:             tok = structure.split('/')
    ...:             txt = ""
    ...:             tree.append(txt.join(tok[1:]))
    ...:         features_tree.append(tree)
    ...:     return features_tree
'''