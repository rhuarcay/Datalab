#Imports
import pyshark
import os
import pickle

MY_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER = '192.168.178.30'
FILE = "nids-train.pcap"

def Conversation_ex(file):

    cap = pyshark.FileCapture(file)
    index_stream = 0
    i = 0
    conversation = []
    s_conversation = ""

    for pkt in cap:
        k_string = ""
        if "FTP" in str(pkt.layers):
            try:
                hex = str(pkt.tcp.payload).replace(':', '')
                stream_index = int(pkt.tcp.stream)
                if index_stream == int(stream_index):
                    k_string = bytes.fromhex(hex).decode('utf-8').replace('\n', '')
                    s_conversation += '\n' + k_string
                else:
                    conversation.append(s_conversation)
                    s_conversation = ""
                    k_string = bytes.fromhex(hex).decode('utf-8').replace('\n', '')
                    s_conversation += '\n' + k_string
                    print("TCP Stream nr: " + str(stream_index) + " done")
                    index_stream = stream_index

            except:
                print("Problem")
    cap.close()
    return conversation

def write_Out_file(out_filename, out_list):
    """ Writes a List in a Outfile in the current directory
        used to store for Exam. the Permissions"""

    with open(out_filename, "wb") as out_file:
        pickle.dump(out_list, out_file)

def main():
    root = os.path.join(MY_DIR, FILE)
    print("Root: " + str(root))
    print("Features are being extracted")
    c_list = Conversation_ex(root)
    write_Out_file("Conversation.txt", c_list)
    #write_Out_file("TestData_Labels.txt", labels)

    print("Features Extraction is done")

    return 0


if __name__ == "__main__":
    main()