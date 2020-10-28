# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:51:49 2020

@author: Rodrigo Huarcaya Alba  Matrikelnr:4919667
         Dennis xx              Matrikelnr:
"""
import email as ml
import zipfile as zipp
import pandas as pd

def extrakt_payload(message):
    global text
    if message.is_multipart():
        for payload in message.get_payload():
            extrakt_payload(payload)
    else:
        text = text + " " + message.get_payload()

emails_Test=[]
email_Test_text=[]

z = zipp.ZipFile('C:/Users/Rodrigo/Desktop/TU-Braunschweig/WS20-21/Datalab/Unit_1/TestDaten/U1_A1_Test.zip')
names = z.namelist()
for name in names:
    email = z.read(name)
    emails_Test.append(email)
for email in emails_Test:
    text=""
    message = ml.message_from_bytes(email)
    extrakt_payload(message)
    email_Test_text.append(text)

print("Test Data is being analysed")
predicted_Test = clf.predict(email_Test_text)
print("Prediction for the Test Date done")

result = []
for i in range(len(names)):
    result.append(names[i]+";"+predicted_Test[i])

df = pd.DataFrame(result, columns=['result'])
export_csv = df.to_csv('export_Prediction_result.csv', index=False,header=False)