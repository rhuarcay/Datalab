# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 16:09:51 2020

@author: Rodrigo
"""
from androguard import misc
from androguard import session
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.analysis.analysis import Analysis
import os
import zipfile as zipp
import pickle
import numpy as np

FILE_VM = 'Testdata_Ex2'
#Features:



def extract_Names(file):
    """Gibt die Namen der Dateien und die Label dazu zurück"""
    file = file + '.zip'
    zf = zipp.ZipFile(file)
    name = zf.namelist()
    return name

def write_Out_file(out_filename, out_list):
    """ Writes a List in a Outfile in the current directory
        used to store for Exam. the Permissions"""    
    
    with open(out_filename, "wb") as out_file:
        pickle.dump(out_list, out_file)

def features_extraction(name_list):
    print("Features werden extrahiert, bitte warten...")
    
    permissions, activity, service, receiver, provider= [],[],[],[],[]
    print(str(len(name_list)) + " Files need to be processed")
    for i, file in enumerate(name_list):
        print("File " + str(i+1) + "/"+ str(len(name_list))+" is been processed")
        
        #get a default session
        sess = misc.get_default_session()
        try:
            a, d, dx = misc.AnalyzeAPK(file) # APK return 3 Elements a ist the 
            d = DalvikVMFormat(a, decompiler='dad')
            dx = Analysis(d)
            
            
            # 54 Permission counts
            permissions.append(a.get_permissions())
            # 55 Activity count
            activity.append(a.get_activities())
            # 56 Service count
            service.append(a.get_services())
            # 57 Receiver count
            receiver.append(a.get_receivers())
            # 58 Provider count
            provider.append(a.get_providers())
            
            sess.reset()
            
            
        except:
            # Permissions need to be filled with 0
            print("error in AnalyzeAPK")
            
            
            permissions.append("")
            activity.append("")
            service.append("")
            receiver.append("")
            provider.append("")
            
            sess.reset()
    
    #End of For

            
    return permissions, activity, service, receiver, provider



def main():
    name_list = extract_Names(FILE_VM)
    permissions, activity, service, receiver, provider = features_extraction(name_list)
    write_Out_file("Permissions_Testdata.txt", permissions)
    write_Out_file("Activity_Testdata.txt", activity)
    write_Out_file("Service_Testdata.txt", service)
    write_Out_file("Receiver_Testdata.txt", receiver)
    write_Out_file("Provider_Testdata.txt", provider)
    
    
    return 0

if __name__ == "__main__":
    main()