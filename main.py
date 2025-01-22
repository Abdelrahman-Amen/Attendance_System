import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Path for test images

path = 'images'
images = []
classNames = []
myList = os.listdir(path)

# Extracting names from the List

for lst in myList:
    curImg = cv2.imread(f'{path}/{lst}')
    images.append(curImg)
    classNames.append(os.path.splitext(lst)[0])
    

# Converting the Images into Encodings

    
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Marking Attendance

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
        

encodeListKnown = findEncodings(images)
print('Encoding Complete')




# Camera Access and Capturing the Face

cap = cv2.VideoCapture(0)
frame_resizing = 0.25

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), fx=frame_resizing, fy=frame_resizing)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        print('matches',matches)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            
            faceLoc = np.array(faceLoc)
            faceLoc = faceLoc / 0.25
            faceLoc=faceLoc.astype(int)
            
            y1, x2, y2, x1 = faceLoc[0], faceLoc[1], faceLoc[2], faceLoc[3]
         
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
 
    cv2.imshow('Webcam',img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()