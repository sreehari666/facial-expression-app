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
from .models import Face

base_dir = settings.BASE_DIR
print(base_dir)

    
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

            face_ = frame[ top-50:bottom+50,left - 50:right+50]
            cv2.rectangle(frame,(f_list[2],f_list[3]),(f_list[0],f_list[1]),(255,255,255),1)
                    
            try:
                face_analysis = DeepFace.analyze(face_)
                print(face_analysis)
                print(face_analysis["dominant_emotion"])
                obj = Face()
                doc = {"retina":resp,"deep":face_analysis,"no_of_faces":len(resp),"dominant_emotion":face_analysis["dominant_emotion"]}
                return doc
            except:
                print("face not detected")
                return 0
    except:
        print("Error retina face")


@gzip.gzip_page
def index(request):
    print("rendering index page")
    data_ = Face.objects.all()
    print(data_[0])
    return render(request, 'pages/index.html',{'data_':data_})

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
            # id_ = '62d9871f43a97aaf1bcdf27c'
            
            
            # obj.emotion = "angry"
            # obj.no_of_faces = 5
            # obj.save()
            
            if ans == 0:
                pass
            else:
                print("-----ans------")
                print(ans)
                Face.objects.filter(id=1).update(emotions=ans["dominant_emotion"])
                Face.objects.filter(id=1).update(no_of_faces=ans["no_of_faces"])

                obj = Face.objects.get(id = 1)
                print("Fetched face object")
                print(obj.emotions)


            

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")



