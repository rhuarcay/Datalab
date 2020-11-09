# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:35:43 2020

@author: guine
"""
FILE = '../Data/Data_Ex1.zip'

import zipfile as zipp
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def extrakt_Names(file):
    zf = zipp.ZipFile(file)
    name = zf.namelist()
    name = name[:-1]
    return name

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

def listlist_to_stringlist(l):
    stringlist = []
    for entry in l:
        string = ''
        for list_entry in entry:
            string = string + ' ' + list_entry
        stringlist.append(string)
    return stringlist

def get_filenames(l):
    string_list = []
    for entry in l:
        for list_entry in entry:
            if (not(list_entry in string_list)):
                string_list.append(list_entry)
    string_list.sort()
    return string_list

def count_filenames(featurelist):
    file_dict = {}
    filelist = get_filenames(featurelist)
    
    for file in filelist:
        file_dict[file] = 0
    
    for entry in featurelist:
        for list_entry in entry:
            file_dict[list_entry] = file_dict[list_entry]+1
            
    return file_dict

#-------------------------------------------------
namelist = []
text = []

namelist = extrakt_Names(FILE)
text = extrakt_Tree(namelist)
#textlist = listlist_to_stringlist(text)
textlist = get_filenames(text)
file_dict = count_filenames(text)
#cv = CountVectorizer(encoding='utf-32')
#cv.fit(textlist)
