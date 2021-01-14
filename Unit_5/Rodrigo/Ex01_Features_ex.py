#Imports
import pyshark
import os
import pickle
import numpy as np


MY_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER = '192.168.178.30'
FILE = "nids-train.pcap"
LOCALDIR = "../Data/nids-train.pcap"
TESTOUTLIER = "../Data/outlier.pcapng"

'''
Features FTP Payload:
(1)- Lenght of Payload DONE
(2)- Number of Words DONE
(3)- Index: (1)/(2) DONE
(4)- Entropy: TODO Methoden zur berechnung von Entropy
(5)- Nonprint Zeichen
(6)- Punkte Zeichen
(7) max lenght Wort
'''

def get_tcp_payload(pkt):
    '''

    :param pkt:
    :return: Bytes in Payload, Number of Words
    '''
    tcp_payload = 0
    bytes_payload = 0
    k_string = ""
    words_in_paylaod = 0
    feature_3 = 0
    try:
        # Hex Darstellung der Payload
        tcp_payload = pkt.tcp.payload
    except Exception as pl:
        print("Problem bei der TCP Payload " + str(pl))

    try:
        #Count bytes in Payload
        bytes_payload = int(str(tcp_payload).count(":")) +1
        #print("Anzahl an Bytes: " + str(bytes_payload))
    except Exception as e0:
        print("Problem bei der Payload_Bytes " + str(e0))

    try:
        #String für die Payload
        hex = str(tcp_payload).replace(':', '')
        k_string = bytes.fromhex(hex).decode('ASCII').replace('\n', '')
        #print("Text : " + k_string)
    except Exception as e1:
        print("Problem bei der Payload_String " + str(e1))

    try:
        #Anzahl an Words bestimmen
        words_in_payload = len(k_string.split())
        #print("Anzahl an Wörter: " + str(words_in_paylaod))
    except Exception as e2:
        print("Problem bei der TCP Payload " + str(e2))

    try:
        #Index Bytes Payload / Words
        feature_3 = int(bytes_payload)/int(words_in_payload)
        #print("Index per Payload : " + str(feature_3))
        #print("_____________________")
    except Exception as e3:
        print("Problem bei der Payload_index " + str(e3))
        print("Payload_byte: " + str(bytes_payload))
        print("String: " + str(k_string))

    return tcp_payload, bytes_payload, k_string, words_in_payload, feature_3


def features_ex(file):

    features = np.empty((139000, 6), dtype=object)

    cap = pyshark.FileCapture(file)
    i = 0
    index_stream = 0
    stream_index = 0

    for pkt in cap:

        k_string = ""
        if "FTP" in str(pkt.layers) and str(pkt.ip.src) != "192.168.178.30":
            #Stream Index für den Packet
            stream_index = int(pkt.tcp.stream)


            #Payload extrahieren
            hex_payload, feature1, s_Payload, feature2, feature3 = get_tcp_payload(pkt)
            #print("TCP_S: " + str(stream_index) + " Packet: " + str(i) + "  Bytes: " + str(feature1) + " Words: " + str(feature2) + " 1/2Index: " + str(feature3))

            features[i, 0] = stream_index # TCP Stream Index Nr.
            features[i, 1] = hex_payload
            features[i, 2] = s_Payload # String Payload
            features[i, 3] = feature1 # Bytes FTP
            features[i, 4] = feature2 # Nr. Words in Payload
            features[i, 5] = feature3 # KPI(Bytes/Index)



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
    write_Out_file("Features.txt", features)
    #write_Out_file("TestData_Labels.txt", labels)

    print("Features Extraction is done")

    return 0


if __name__ == "__main__":
    main()