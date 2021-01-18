#Imports
import pyshark
import os
import pickle
import numpy as np
import re


MY_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER = '192.168.178.30'
FILE = "nids-train.pcap"
LOCALDIR = "../Data/nids-train.pcap"
TESTOUTLIER = "../Data/outlier.pcapng"
__ERRORLIST = []

'''
Features FTP Payload:
(1)- Lenght of Payload DONE
(2)- Number of Words DONE
(3)- Index: (1)/(2) DONE
(4)- Entropy: TODO Methoden zur berechnung von Entropy
(5)- Nonprint Zeichen DONE
(6)- Punkte Zeichen DONE
'''

def get_tcp_payload(pkt, tcpstream):
    '''

    :param pkt:
    :return: Bytes in Payload, Number of Words
    '''
    tcp_payload = 0
    bytes_payload = 0
    k_string = ""
    words_in_payload = 0
    words = 0
    feature_3 = 0
    nonprint = 0
    delimeter = "/","_", " ", "-", ",", ".", "\\"
    regexPattern = '|'.join(map(re.escape, delimeter))
    
    try:
        # Hex Darstellung der Payload
        tcp_payload = pkt.tcp.payload
    except Exception as pl:
        print("Problem bei der TCP Payload " + str(pl))
        set_error_list(str(pl), tcpstream)

    try:
        #Count bytes in Payload
        bytes_payload = int(str(tcp_payload).count(":")) +1
        #print("Anzahl an Bytes: " + str(bytes_payload))
    except Exception as e0:
        print("Problem bei der Payload_Bytes " + str(e0))
        set_error_list(str(e0), tcpstream)

    try:
        #String für die Payload
        hex = str(tcp_payload).replace(':', '')
        k_string = bytes.fromhex(hex).decode('ASCII').replace('\n', '')
        #print("Text : " + k_string)
    except Exception as e1:
        print("Problem bei der Payload_String " + str(e1))
        set_error_list(str(e1), tcpstream)

    try:
        #Anzahl an Words bestimmen
        words_in_payload = len(re.split(regexPattern, k_string))
        #print("Anzahl an Wörter: " + str(words_in_paylaod))
    except Exception as e2:
        print("Problem bei der TCP Payload " + str(e2))
        set_error_list(str(e2), tcpstream)

    try:
        #Index Bytes Payload / Words
        feature_3 = int(bytes_payload)/int(words_in_payload)
        #print("Index per Payload : " + str(feature_3))
        #print("_____________________")
    except Exception as e3:
        print("Problem bei der Payload_index " + str(e3))
        print("Payload_byte: " + str(bytes_payload))
        print("String: " + str(k_string))
        set_error_list(str(e3), tcpstream)
        
    try:
        #Anzahl an Punkte im Payload
        punkts_in_payload = str(tcp_payload).count("2e")
    except Exception as e6:
        print("Problem bei der Anzahl an Nullwerte " + str(e6))
        set_error_list(str(e6), tcpstream)
        
    #Now loop für alle characters in 
    for char in str(tcp_payload).split(":"):
        try:
            bytes.fromhex(char).decode('ASCII')
        except:
            nonprint += 1
            
    return tcp_payload, bytes_payload, k_string, words_in_payload, feature_3, nonprint, punkts_in_payload

def set_error_list(error, tcpstream):
    err = str(tcpstream) + " -- " + str(error)
    __ERRORLIST.append(err)
    
    

def features_ex(file):

    features = np.empty((138022, 8), dtype=object)

    cap = pyshark.FileCapture(file)
    i = 0
    index_stream = 0
    stream_index = 0

    for pkt in cap:

        k_string = ""
        if "FTP" in str(pkt.layers) and str(pkt.ip.src) != "192.168.178.30" and str(pkt.tcp.payload).strip() != "0d:0a":
            #Stream Index für den Packet
            stream_index = int(pkt.tcp.stream)


            #Payload extrahieren
            hex_payload, feature1, s_Payload, feature2, feature3, feature5, feature6 = get_tcp_payload(pkt, stream_index)
            #print("TCP_S: " + str(stream_index) + " Packet: " + str(i) + "  Bytes: " + str(feature1) + " Words: " + str(feature2) + " 1/2Index: " + str(feature3))

            features[i, 0] = stream_index # TCP Stream Index Nr.
            features[i, 1] = str(hex_payload).strip()
            features[i, 2] = s_Payload.strip() # String Payload
            features[i, 3] = int(feature1) # Bytes FTP
            features[i, 4] = int(feature2) # Nr. Words in Payload
            features[i, 5] = int(feature3) # KPI(Bytes/Index)
            features[i, 6] = int(feature5) # Non Printable Char
            features[i, 7] = int(feature6) # Punkte im Text


            i += 1

        if stream_index != index_stream:
            print("TCP Stream DONE: " + str(stream_index))
            index_stream = stream_index

    cap.close()
    return features

def write_Out_file(out_filename, out_list):
    """ Writes a List in a Outfile in the current directory
        used to store for Exam. the Permissions"""

    with open(out_filename, "wb") as out_file:
        pickle.dump(out_list, out_file)

def main():
    root = os.path.join(MY_DIR, FILE)
    print("Root: " + str(root))
    print("Features are being extracted")
    features = features_ex(root)
    write_Out_file("Features.txt", features) # Features List
    write_Out_file("Errors.txt", __ERRORLIST) # Error List

    print("Features Extraction is done")

    return 0


if __name__ == "__main__":
    main()