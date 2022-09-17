from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from deepface import DeepFace
from retinaface import RetinaFace
from PIL import Image
import os
from django.conf import settings
from numpy import asarray
from .models import Face_static
from .models import Face
from .models import ReportData
from django.http import JsonResponse
from datetime import datetime

base_dir = settings.BASE_DIR
print(base_dir)


def get_deepData(face_frame):
    try:
        face_analysis = DeepFace.analyze(face_frame)
        return face_analysis
    except:
        print("deep face failed!!!!")
        return 0

def insertData(face_count,no_of_face,frame_face):
    print("call--")
    print(face_count)
    face_analysis = get_deepData(frame_face)
    if face_analysis == 0:
        print("deep failed returned 0")
        return -1
    else:
        obj = ReportData(emotion = face_analysis["dominant_emotion"],date=datetime.now())
        obj.save()
        try:
            print(Face.objects.get(face_id = face_count))
            Face.objects.filter(face_id=face_count).update(emotions=face_analysis["dominant_emotion"])
            Face.objects.filter(face_id=face_count).update(no_of_faces=no_of_face)
            
            return 0
        except:
            face_analysis = DeepFace.analyze(frame_face)
            b = Face(face_id=face_count,no_of_faces=no_of_face,emotions=face_analysis["dominant_emotion"])
            
            b.save()
            return 1
 
def detect(frame):
    resp = RetinaFace.detect_faces(frame)
    print(resp)
    print(len(resp))

    try:
        for face in resp:
            f = resp[face]
            print(f["facial_area"])   
            f_list = f["facial_area"]
                
            left = f_list[0]
            top = f_list[1] 
            right = f_list[2] 
            bottom = f_list[3] 
            count = int(face[5])
            # count = 2
            face_ = frame[ top-60:bottom+60,left - 60:right+60]
            cv2.rectangle(frame,(f_list[2],f_list[3]),(f_list[0],f_list[1]),(255,255,255),1)
            # print(face)
            result = insertData(count,len(resp),face_)
            Face_static.objects.filter(id = 1).update(no_of_faces=len(resp))
            if count == len(resp):
                return result
            
    except:
        print("Error retina face")
        return 0


@gzip.gzip_page
def index(request):
    print("rendering index page")
    Face.objects.all().delete()
    Face_static.objects.filter(id = 1).update(no_of_faces=0)
    return render(request, 'pages/index.html')

#to capture video class
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            ans = detect(self.frame)
            if ans == 0:
                pass
            else:
                print("-----ans------")
                print(ans)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

def getData(request):
    angry = 0
    fear = 0
    neutral = 0
    sad = 0
    happy = 0 
    surprise = 0
    disgust = 0
    
    data_ = Face.objects.all()[:20]
    for obj in data_:
        if obj.emotions == 'angry':
            angry += 1
        if obj.emotions == 'fear':
            fear += 1
        if obj.emotions == 'neutral':
            neutral += 1
        if obj.emotions == 'sad':
            sad += 1
        if obj.emotions == 'happy':
            happy += 1
        if obj.emotions == 'surprise':
            surprise += 1
        if obj.emotions == 'disgust':
            disgust += 1
    list_ = [angry,fear,neutral,sad,happy,surprise,disgust]
    temp = Face_static.objects.get(id = 1)
    return JsonResponse({'data':list(data_.values()),'no_of_faces':temp.no_of_faces,'emotion_list':list_})