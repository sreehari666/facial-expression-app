# facial-expression-app
 
About the project

Technology is improving day by day and improving productivity in various fields so it has to make
improvements in teaching profession also. Nowadays teachers teach in classrooms and go. They don’t
get a view about how students interpret their classes or also whether they are interested in their teaching.
This project is to make a system that helps teachers to get the view on how students react to their teaching.
Here we use detect the facial expressions of students sitting in classrooms and then analyze the emotions
of students from it. The emotions shown by these students represent how they are sitting in classrooms
while teachers are teaching. Camera installed in classroom capture the video of students sitting in the
classrooms which are fed to the system which detect the facial emotions of students and make a report of
the data which can be accessed by teachers or other school authorities from the website.
The difference between the teaching effectiveness in case where teachers teach as usual and when they
analyze the reportshowing the emotions ofstudentsin class and then prepare teaching according to the data
and case where they teach as usual has drastic difference. The teaching strategies changed by analysing
the data from the system shows much improvement.

Facial Expression Detection is a technology that analyses facial expression from both static images and
videos in order to reveal information on one’s emotional state. Facial Emotion Recognition is a technology
used for analying sentiments by different sources, such as pictures and videos.
This project helps to improve the classes of teachers by helping them get the report that shows the overall
emotions of students sitting in the class. Mental health of students is very important in academics, inorder
to know how students are behaving in the class is very important to a teacher .Through this project teachers
can get an overview of overall behaviour of the class, this helps them to improve their teaching strategies
hence improve academic as well as extra curricular activities of students.
The live visual from the camera is fed to the web server frame by frame,and each frame is processed
individually and it will first detect all faces in the frame, then each face is passed to deepface analysis and
get the information related to facial expression of each face.These information is processed for real time
displaying of information in the front end.Also the informations are stored in a database for report
generation.

![out_2](https://user-images.githubusercontent.com/61986594/190860731-3490f503-f328-408f-ab19-9eebf2514449.png)






![report_out1](https://user-images.githubusercontent.com/61986594/190860746-4f685bb9-f46e-47ed-b9a1-6b1e52e9ee3e.png)

To run this app in your system:

open command prompt and execute the following command

1 . git clone https://github.com/sreehari666/facial-expression-app.git or download the zip file and extract it

2 . cd facial-expression-app

3 . pip install virtualenv

4 . virtualenv -p python3 venv

5 . pip install -r requirements.txt

6 . python manage.py runserver
