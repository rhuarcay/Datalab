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

FILE_VM = 'Data_Ex2'
#Features:



def extract_Names(file):
    """Gibt die Namen der Dateien und die Label dazu zurück"""
    file = file + '.zip'
    zf = zipp.ZipFile(file)
    name = zf.namelist()[:-1]
    return name

def write_Out_file(out_filename, out_list):
    """ Writes a List in a Outfile in the current directory
        used to store for Exam. the Permissions"""    
    
    with open(out_filename, "wb") as out_file:
        pickle.dump(out_list, out_file)

def features_extraction(name_list):
    print("Features werden extrahiert, bitte warten...")
    
    FEATURES = np.zeros((len(name_list), 59))
    print(str(len(name_list)) + " Files need to be processed")
    for i, file in enumerate(name_list):
        print("File " + str(i+1) + "/"+ str(len(name_list))+" is been processed")
        features = analyseAPK(i, file)
        for j in range(0,59):
            FEATURES[i,j] = features[0,j]
        
    return FEATURES

def analyseAPK(i, file):
    # Features 1-5
    apk_size, dex_size, min_andr_ver, max_andr_ver, target_andr_ver = 0,0,0,0,0
    method_count, class_count, crypto_count, dynCode_count, native_count = 0,0,0,0,0
    reflect_count, file_count, sendSMS, deleteSMS, interruptSMS = 0,0,0,0,0
    httpPost, deviceId, simCountry, installedPkg, subprocess = 0,0,0,0,0
    jni, button_count, textView_count, editView_count, imageButton_count = 0,0,0,0,0
    checkBox_count, radioGroup_count, radioButton_count, toast_count, spinner_count = 0,0,0,0,0 
    listView_count, internet, set_debug_app, modiphy_phone_state, record_audio = 0,0,0,0,0
    receive_boot_completed, receive_mms, receive_sms, receive_wap_push, send_sms = 0,0,0,0,0
    call_phone, call_privileged, process_outgoing_calls, read_call_log, read_external_storage = 0,0,0,0,0
    read_logs, access_coarse_location, access_fine_location, bluetooth, camera = 0,0,0,0,0
    install_packages, nfc, read_contacts, permission_count, activity_count = 0,0,0,0,0
    service_count, receiver_count, provider_count, exported_count = 0,0,0,0
    features = np.zeros((1,59))
    
    apk_zip = zipp.ZipFile(file)
    apk_size = os.path.getsize(file) # 1
    dex_size = apk_zip.getinfo('classes.dex').file_size # 2
    
    #get a default session
    sess = misc.get_default_session()
    try:
        a, d, dx = misc.AnalyzeAPK(file) # APK return 3 Elements a ist the 
        d = DalvikVMFormat(a, decompiler='dad')
        dx = Analysis(d)
    
    except:
        # Permissions need to be filled with 0
        features[0,0],features[0,1],features[0,2],features[0,3],features[0,4]= apk_size, dex_size, min_andr_ver, max_andr_ver, target_andr_ver
        features[0,5],features[0,6],features[0,7],features[0,8],features[0,8]= method_count, class_count, crypto_count, dynCode_count, native_count
        features[0,10],features[0,11],features[0,12],features[0,13],features[0,14]= reflect_count, file_count, sendSMS, deleteSMS, interruptSMS
        features[0,15],features[0,16],features[0,17],features[0,18],features[0,19]= httpPost, deviceId, simCountry, installedPkg, subprocess
        features[0,20],features[0,21],features[0,22],features[0,23],features[0,24]= jni, button_count, textView_count, editView_count, imageButton_count
        features[0,25],features[0,26],features[0,27],features[0,28],features[0,29]= checkBox_count, radioGroup_count, radioButton_count, toast_count, spinner_count
        features[0,30],features[0,31],features[0,32],features[0,33],features[0,34]= listView_count, internet, set_debug_app, modiphy_phone_state, record_audio
        features[0,35],features[0,36],features[0,37],features[0,38],features[0,39]= receive_boot_completed, receive_mms, receive_sms, receive_wap_push, send_sms
        features[0,40],features[0,41],features[0,42],features[0,43],features[0,44]= call_phone, call_privileged, process_outgoing_calls, read_call_log, read_external_storage
        features[0,45],features[0,46],features[0,47],features[0,48],features[0,49]= read_logs, access_coarse_location, access_fine_location, bluetooth, camera
        features[0,50],features[0,51],features[0,52],features[0,53],features[0,54]= install_packages, nfc, read_contacts, permission_count, activity_count
        features[0,55],features[0,56],features[0,57],features[0,58]= service_count, receiver_count, provider_count, exported_count
        print("error in AnalyzeAPK")
        sess.reset()
        return features
            
    # 3 Min Android Version
    if a.get_min_sdk_version() is not None:
        min_andr_ver = str(a.get_min_sdk_version())
    else:
        min_andr_ver = 0
    # 4 Max Android Version
    if a.get_max_sdk_version() is not None:
        max_andr_ver = str(a.get_max_sdk_version())
    else:
        max_andr_ver = 0
    # 5 Target SDK Version
    if a.get_target_sdk_version() is not None:
        target_andr_ver = str(a.get_target_sdk_version())
    else:
        target_andr_ver = 0
    
    # 6 Methods Counts
    method_count = d.get_len_methods()
    # 7 Class Counts
    class_count = len(d.get_classes())
    """
    # 8 Crypto_count
    crypto_count = len(dx.find_methods('Ljava/crypto/.', '.', '.'))
    # 9
    dynCode_count = len(dx.get_tainted_packages().search_methods('Ldalvik/system/DexClassLoader/.', '.', '.'))
    # 10
    native_count = len(dx.get_tainted_packages().search_methods('Ljava/lang/System;', '.', '.'))
    # 11
    reflect_count = len(dx.get_tainted_packages().search_methods('Ljava/lang/reflect/Method;', '.', '.'))
    """
    # 12 File Count
    file_count = len(a.get_files())
    
    """
    # API Features
    # 13 sendSMS
    if (len(dx.get_tainted_packages().search_methods('Landroid/telephony/SmsManager;', 'send[a-zA-Z]+Message', '.')) > 0) or (len(dx.get_tainted_packages().search_methods('Landroid/telephony/gsm/SmsManager;', 'send[a-zA-Z]+Message', '.')) > 0):
        sendSMS = 1
    else:
        sendSMS = 0
    # 14 deleteSMS
    if len(dx.get_tainted_packages().search_methods('Landroid/content/ContentResolver;', 'delete', '')) > 0:
        deleteSMS = 1
    else:
        deleteSMS = 0
    # 15 interruptSMS
    if len(dx.get_tainted_packages().search_methods('Landroid/content/BroadcastReceiver;', 'abortBroadcast', '.')) > 0:
        interruptSMS = 1
    else:
        interruptSMS = 0
    # 16 httpPost
    if (len(dx.get_tainted_packages().search_methods('Lorg/apache/http/client/methods/HttpPost;', '.', '.')) > 0) or (len(dx.get_tainted_packages().search_methods('Ljava/net/HttpURLConnection;', '.', '.')) > 0):
        httpPost = 1
    else:
        httpPost = 0
    # 17 deviceId
    if len(dx.get_tainted_packages().search_methods('Landroid/telephony/TelephonyManager;', 'getDeviceId', '.')) > 0:
        deviceId = 1
    else:
        deviceId = 0
    # 18 simCountry
    if len(dx.get_tainted_packages().search_methods('Landroid/telephony/TelephonyManager;', 'getSimCountryIso', '.')) > 0:
        simCountry = 1
    else:
        simCountry = 0
    # 19 installedPkg
    if len(dx.get_tainted_packages().search_methods('Landroid/content/pm/PackageManager;', 'getInstalledPackages', '.')) > 0:
        installedPkg = 1
    else:
        installedPkg = 0

    # 20 subprocess
    if (len(dx.get_tainted_packages().search_methods('Ljava/lang/ProcessBuilder;','start','.')) > 0) or (len(dx.get_tainted_packages().search_methods('Ljava/lang/Runtime;','exec','.')) > 0):
        subprocess = 1
    else:
        subprocess = 0
    # 21 jni
    if len(dx.get_tainted_packages().search_methods('Ljava/lang/System;', 'loadLibrary', '.')) > 0:
        jni = 1
    else:
        jni = 0

    # Widget features
    fields = dx.get_tainted_fields()
    field_list = []
    for field in fields:
        field_list.append(field)
    # Initiallisierung der bekante Widgets:
    # 22             23               24                25             26               27                28                29            30             31 
    for field in field_list:
        if 'Landroid/widget/Button;' in field[1]:
            button_count += 1
        elif 'Landroid/widget/TextView;' in field[1]:
            textView_count += 1
        elif 'Landroid/widget/EditText;' in field[1]:
            editView_count += 1
        elif 'Landroid/widget/ImageButton;' in field[1]:
            imageButton_count += 1
        elif 'Landroid/widget/CheckBox;' in field[1]:
            checkBox_count += 1
        elif 'Landroid/widget/RadioGroup;' in field[1]:
            radioGroup_count += 1
        elif 'Landroid/widget/RadioButton;' in field[1]:
            radioButton_count += 1
        elif 'Landroid/widget/Toast;' in field[1]:
            toast_count += 1
        elif 'Landroid/widget/Spinner;' in field[1]:
            spinner_count += 1
        elif 'Landroid/widget/ListView;' in field[1]:
            listView_count += 1
    """
    
    # Permissions
    # Permission features
    # 32 INTERNET
    if 'android.permission.INTERNET' in a.get_permissions():
        internet = 1
    else:
        internet = 0
    # 33 SET_DEBUG_APP
    if 'android.permission.SET_DEBUG_APP' in a.get_permissions():
        set_debug_app = 1
    else:
        set_debug_app = 0
    # 34 MODIFY_PHONE_STATE
    if 'android.permission.MODIFY_PHONE_STATE' in a.get_permissions():
        modiphy_phone_state = 1
    else:
        modiphy_phone_state = 0
    # 35 RECORD_AUDIO
    if 'android.permission.RECORD_AUDIO' in a.get_permissions():
        record_audio = 1
    else:
        record_audio = 0
    # 36 RECEIVE_BOOT_COMPLETED
    if 'android.permission.RECEIVE_BOOT_COMPLETED' in a.get_permissions():
        receive_boot_completed = 1
    else:
        receive_boot_completed = 0
    # 37 RECEIVE_MMS
    if 'android.permission.RECEIVE_MMS' in a.get_permissions():
        receive_mms = 1
    else:
        receive_mms = 0
    # 38 RECEIVE_SMS
    if 'android.permission.RECEIVE_SMS' in a.get_permissions():
        receive_sms = 1
    else:
        receive_sms = 0
    # 39 RECEIVE_WAP_PUSH
    if 'android.permission.RECEIVE_WAP_PUSH' in a.get_permissions():
        receive_wap_push = 1
    else:
        receive_wap_push = 0
    # 40 SEND_SMS
    if 'android.permission.SEND_SMS' in a.get_permissions():
        send_sms = 1
    else:
        send_sms = 0
    # 41 CALL_PHONE
    if 'android.permission.CALL_PHONE' in a.get_permissions():
        call_phone = 1
    else:
        call_phone = 0
    # 42 CALL_PRIVILEGED
    if 'android.permission.CALL_PRIVILEGED' in a.get_permissions():
        call_privileged = 1
    else:
        call_privileged = 0
    # 43 PROCESS_OUTGOING_CALLS
    if 'android.permission.PROCESS_OUTGOING_CALLS' in a.get_permissions():
        process_outgoing_calls = 1
    else:
        process_outgoing_calls = 0
    # 44 READ_CALL_LOG
    if 'android.permission.READ_CALL_LOG' in a.get_permissions():
        read_call_log = 1
    else:
        read_call_log = 0
    # 45 READ_EXTERNAL_STORAGE
    if 'android.permission.READ_EXTERNAL_STORAGE' in a.get_permissions():
        read_external_storage = 1
    else:
        read_external_storage = 0
    # 46 READ_LOGS
    if 'android.permission.READ_LOGS' in a.get_permissions():
        read_logs = 1
    else:
        read_logs = 0
    # 47 ACCESS_COARSE_LOCATION
    if 'android.permission.ACCESS_COARSE_LOCATION' in a.get_permissions():
        access_coarse_location = 1
    else:
        access_coarse_location = 0
    # 48 ACCESS_FINE_LOCATION
    if 'android.permission.ACCESS_FINE_LOCATION' in a.get_permissions():
        access_fine_location = 1
    else:
        access_fine_location = 0
    # 49 BLUETOOTH
    if 'android.permission.BLUETOOTH' in a.get_permissions():
        bluetooth = 1
    else:
        bluetooth = 0
    # 50 CAMERA
    if 'android.permission.CAMERA' in a.get_permissions():
        camera = 1
    else:
        camera = 0
    # 51 INSTALL_PACKAGES
    if 'android.permission.INSTALL_PACKAGES' in a.get_permissions():
        install_packages = 1
    else:
        install_packages = 0
    # 52 NFC
    if 'android.permission.NFC' in a.get_permissions():
        nfc = 1
    else:
        nfc = 0
    # 53 READ_CONTACTS
    if 'android.permission.READ_CONTACTS' in a.get_permissions():
        read_contacts = 1
    else:
        read_contacts = 0
    
    # 54 Permission counts
    permission_count = len(a.get_permissions())
    # 55 Activity count
    activity_count = len(a.get_activities())
    # 56 Service count
    service_count = len(a.get_services())
    # 57 Receiver count
    receiver_count = len(a.get_receivers())
    # 58 Provider count
    provider_count = len(a.get_providers())
    
    # 59 Exported count
    """    
    for activity in a.get_android_manifest_xml().getElementsByTagName('activity'):
        if activity.getAttribute('android:exported') == 'true':
            exported_count += 1
    for service in a.get_android_manifest_xml().getElementsByTagName('service'):
        if activity.getAttribute('android:exported') == 'true':
            exported_count += 1
    for receiver in a.get_android_manifest_xml().getElementsByTagName('receiver'):
        if activity.getAttribute('android:exported') == 'true':
            exported_count += 1
    for provider in a.get_android_manifest_xml().getElementsByTagName('provider'):
        if activity.getAttribute('android:exported') == 'true':
            exported_count += 1
    """
    
    #Fill the array
    features[0,0],features[0,1],features[0,2],features[0,3],features[0,4]= apk_size, dex_size, min_andr_ver, max_andr_ver, target_andr_ver
    features[0,5],features[0,6],features[0,7],features[0,8],features[0,8]= method_count, class_count, crypto_count, dynCode_count, native_count
    features[0,10],features[0,11],features[0,12],features[0,13],features[0,14]= reflect_count, file_count, sendSMS, deleteSMS, interruptSMS
    features[0,15],features[0,16],features[0,17],features[0,18],features[0,19]= httpPost, deviceId, simCountry, installedPkg, subprocess
    features[0,20],features[0,21],features[0,22],features[0,23],features[0,24]= jni, button_count, textView_count, editView_count, imageButton_count
    features[0,25],features[0,26],features[0,27],features[0,28],features[0,29]= checkBox_count, radioGroup_count, radioButton_count, toast_count, spinner_count
    features[0,30],features[0,31],features[0,32],features[0,33],features[0,34]= listView_count, internet, set_debug_app, modiphy_phone_state, record_audio
    features[0,35],features[0,36],features[0,37],features[0,38],features[0,39]= receive_boot_completed, receive_mms, receive_sms, receive_wap_push, send_sms
    features[0,40],features[0,41],features[0,42],features[0,43],features[0,44]= call_phone, call_privileged, process_outgoing_calls, read_call_log, read_external_storage
    features[0,45],features[0,46],features[0,47],features[0,48],features[0,49]= read_logs, access_coarse_location, access_fine_location, bluetooth, camera
    features[0,50],features[0,51],features[0,52],features[0,53],features[0,54]= install_packages, nfc, read_contacts, permission_count, activity_count
    features[0,55],features[0,56],features[0,57],features[0,58]= service_count, receiver_count, provider_count, exported_count
    
    return features

def main():
    name_list = extract_Names(FILE_VM)
    FEATURES = features_extraction(name_list)
    write_Out_file("FEATURES.txt", FEATURES)
    
    return 0

if __name__ == "__main__":
    main()