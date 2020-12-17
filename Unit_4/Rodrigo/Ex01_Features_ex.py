# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:17:00 2020

@author: Rodrigo
"""
import numpy as np
import zipfile as zipp
import pickle
import pyshark
import os

MY_DIR = os.path.dirname(os.path.abspath(__file__))
ENTRY = "134.169.109.51"
CLIENT = "134.169.109.25"

def total_sizes(cap):
    t_out = 0
    t_in = 0
    t_num = 0
    no_out = 0
    no_in = 0
    pck_size = []

    for pkt in cap:
        len = int(pkt.captured_length)
        t_num += 1

        try:
            ip = pkt.ip.src

            if ip == ENTRY:
                t_out += len
                no_out += 1
                len = len*-1
            else:
                t_in += len
                no_in += 1
        except:
            print("Problem with Package nr. " + str(t_num) + " in " + str(cap.input_filename))
            t_in += len
            no_in += 1

        if t_num <= 40:
            pck_size.append(len)

    return t_out, t_in, t_num, no_out, no_in, pck_size

def features_ex(root):
    count = 0
    label = []
    tOutSizes, tInSizes, tNumPack, noOutPack, noInPack = [], [], [], [], []
    ratio, packSizes = [], []
    f = ""
    for path, subdirs, files in os.walk(root):
        for name in files:
            l_name = ""
            print("FILE Nr. " + str(count) + " is been processed, please wait")
            count +=1
            file = os.path.join(path, name)
            l_name = name.split("_")[0]
            cap = pyshark.FileCapture(file)
            total_outcoming_sizes, total_incoming_sizes, total_number_packets, no_outgoing_packets, no_incoming_packets, pack_sizes = total_sizes(
                cap)
            ratio_incoming_outgoing = no_outgoing_packets / no_incoming_packets

            label.append(l_name)
            tOutSizes.append(total_outcoming_sizes)
            tInSizes.append(total_incoming_sizes)
            tNumPack.append(total_number_packets)
            noOutPack.append(no_outgoing_packets)
            noInPack.append(no_incoming_packets)
            ratio.append(ratio_incoming_outgoing)
            packSizes.append(pack_sizes)

            """"
            print(tOutSizes)
            print(tInSizes)
            print(tNumPack)
            print(noOutPack)
            print(noInPack)
            print(ratio)
            print(packSizes)
            """
            cap.close()

    features = np.zeros((count, 46))
    for i in range(0, count):
        features[i, 0] = tOutSizes[i]
        features[i, 1] = tInSizes[i]
        features[i, 2] = tNumPack[i]
        features[i, 3] = noOutPack[i]
        features[i, 4] = noInPack[i]
        features[i, 5] = ratio[i]

        for j in range(6,46):
            features[i,j] = packSizes[i][j-6]


    #print(features)

    return features, label


def write_Out_file(out_filename, out_list):
    """ Writes a List in a Outfile in the current directory
        used to store for Exam. the Permissions"""

    with open(out_filename, "wb") as out_file:
        pickle.dump(out_list, out_file)

def main():
    root = os.path.join(MY_DIR, "Data")
    print("Root: " + str(root))
    print("Features are being extracted")
    features, labels = features_ex(root)
    write_Out_file("Features.txt", features)
    write_Out_file("Labels.txt", labels)

    print("Features Extraction is done")

    return 0

if __name__ == "__main__":
    main()
    