from django.shortcuts import render
from facialexpression.models import ReportData
from django.http import JsonResponse

# Create your views here.
def report(request):
    
    return render(request,'pages/report.html',)

def getReport(request):
    data_ = ReportData.objects.all()
    angry = 0
    fear = 0
    neutral = 0
    sad = 0
    happy = 0 
    surprise = 0
    disgust = 0
    
    for obj in data_:
        if obj.emotion == 'angry':
            angry += 1
        if obj.emotion == 'fear':
            fear += 1
        if obj.emotion == 'neutral':
            neutral += 1
        if obj.emotion == 'sad':
            sad += 1
        if obj.emotion == 'happy':
            happy += 1
        if obj.emotion == 'surprise':
            surprise += 1
        if obj.emotion == 'disgust':
            disgust += 1
    list_ = [angry,fear,neutral,sad,happy,surprise,disgust]
    ind = list_.index(max(list_))
    
    if ind == 0:
        dominant_emotion = "angry"
    if ind == 1:
        dominant_emotion = "fear"
    if ind == 2:
        dominant_emotion = "neutral"
    if ind == 3:
        dominant_emotion = "sad"
    if ind == 4:
        dominant_emotion = "happy"
    if ind == 5:
        dominant_emotion = "surprise"
    if ind == 6:
        dominant_emotion = "disgust"
    

    return JsonResponse({'emotion_list':list_,"dominant_emotion":dominant_emotion})

