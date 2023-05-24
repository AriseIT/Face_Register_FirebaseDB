import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
 
''' Importing student images'''

folderPath = 'Images'

imgList = []
studentIds = []

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

def imgUpload(path):
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
    print(studentIds, fileName)
    print("Encoding Started ...")
    
    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    
    print("Encoding Complete")
    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    os.remove(os.path.join(folderPath, path))
    print("File Saved")