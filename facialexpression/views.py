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

base_dir = settings.BASE_DIR
print(base_dir)

    
def detect(frame):
    resp = RetinaFace.detect_faces(frame)
    print(resp)

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
            
            doc = {"retina":resp,"deep":face_analysis}
            return doc
        except:
            print("face not detected")
            return 0


@gzip.gzip_page
def index(request):
    
    return render(request, 'pages/index.html',{'price':300})

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
                print(ans)

            

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")



