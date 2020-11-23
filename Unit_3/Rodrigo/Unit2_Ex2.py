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

MY_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = 'Data_Ex2'
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

def write_Out_file(out_filename, out_text):
    """ Writes a Text/List in a Outfile in the current directory
        used to store for Exam. the Permissions"""    
    
    with open(out_filename, "wt") as out_file:
        out_file.write(out_text)

def write_In_file(in_file):
    """Writes a Text/List to an outfile in the current directory"""
    with open(in_file, "r") as in_file:    
        text = in_file.read()
    
    return text


def main():
    
    name_list = extract_Names(FILE)
    labels_list = extract_Labels(name_list)
    print(len(name_list))
    print(len(labels_list))    
    permissions = []
    
    print("Permissions werden extrahiert, bitte warten...")
    print("0/1000")
    i = 0 
    
    for file in name_list:
        
        # get a default session
        sess = misc.get_default_session()
        try:
            a, d, dx = misc.AnalyzeAPK(file) # APK return 3 Elements a ist the 
        
            permissions.append(a.get_permissions())
            sess.reset()
        except:    
            sess.reset()
        
        i+=1
        print(str(i)+"/1000 has been processed")
        
        
    print("Permissions already processed")
    print("Saving Permissions...")
    
    write_Out_file("Permissions.txt", permissions)

    return 0



if __name__ == "__main__":
    main()