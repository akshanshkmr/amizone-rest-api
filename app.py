import requests
import bs4
from flask import Flask,request
from datetime import datetime as date

URL         = "https://s.amizone.net"
URL_LOGIN   = "https://student.amizone.net/Login/Login"
URL_HOME    = "https://s.amizone.net/Home"

class Cookies:
    def saveCookie(self,requestsCookieJar):
        self.cookies=requestsCookieJar

    def login(self,user,pwd):
        s= requests.Session()
        s.headers.update({"Referer":URL})
        defaultPage=s.get(URL)
        htmlObject = bs4.BeautifulSoup(defaultPage.content,'html.parser')
        rvt = htmlObject.find(id="loginform").input['value']
        data = {
            "_UserName": user,
            "_Password": pwd,
            "__RequestVerificationToken": rvt
        }
        logged = s.post(URL,data=data)
        self.saveCookie(s.cookies)
        if(logged.url==URL_HOME):
            return 200
        else:
            return 404

r = requests.Session()
r.headers.update({"Referer": URL})
c = Cookies()

def login(usr,pwd):
    s=c.login(usr,pwd)
    r.cookies = c.cookies
    if s==200:
        return "Login Successful"
    else:
        return "Incorrect Username or Password"

def my_profile(uname):
    a = r.get("https://student.amizone.net/Home/")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    data=b.find("span",attrs={"class":"user-info"}).text.strip().split(' ')
    Enrollment=data.pop()
    name=''
    img = "https://amizone.net/amizone/Images/Signatures/" + uname + "_P.png"
    for i in data:
        name+=i+' '
    return {
        "Name":name,
        "Enrollment":Enrollment,
        "ImgUrl":img
    }


def my_courses():
    a = r.get("https://student.amizone.net/Academics/MyCourses?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
    courseName = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Name"})]
    attendance = [c.text.strip() for c in b.find_all(attrs={'data-title': "Attendance"})]
    syllabus   = [c.decode_contents() for c in b.find_all(attrs={'data-title': "Course Syllabus"})]
    # this returned a list(string) of anchor tags so the below code is to extract href from it
    syllabus   = [i[i.find('"')+1:i.find('"',i.find('"')+1)] for i in syllabus]
    # percentage = [float(i[i.find("(")+1:i.find(")")]) for i in attendance]
    percentage=[]
    for i in attendance:
        try:
            x=float(i[i.find("(")+1:i.find(")")])
            percentage.append(x)
        except:
<<<<<<< HEAD
            percentage.append(100.0)
=======
            percentage.append(0.0)
>>>>>>> 4f6e7b68398351c5ff34c6b9ba91b32aeb971542
    return {
        "CourseCode":courseCode,
        "CourseName":courseName,
        "Attendance":attendance,
        "Syllabus":syllabus,
        "Percentage":percentage
    }


def results():
    a=r.get("https://student.amizone.net/Examination/Examination?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
    courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
    GradeObtained = [c.text.strip() for c in b.find_all(attrs={'data-title': "Go"})]
    GradePoint=[c.text.strip() for c in b.find_all(attrs={'data-title': "GP"})]
    sgpa=[float(x.text.strip()) for x in b.find_all(attrs={'data-title': "SGPA"})]
    cgpa=[x.text.strip() for x in b.find_all(attrs={'data-title': "CGPA"})]
    cgpa[0] = sgpa[0]
    cgpa=[float(x) for x in cgpa]
    return {
        "Latest Result":{
            "courseCode":courseCode,
            "courseTitle":courseTitle,
            "Go":GradeObtained,
            "GP":GradePoint,
        },
        "Combined":{
            "sgpa":sgpa,
            "cgpa":cgpa
        }
    }

def my_faculty():
    a=r.get("https://student.amizone.net/FacultyFeeback/FacultyFeedback?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    faculties=[x.text.strip() for x in b.find_all(attrs={"class":"faculty-name"})]
    subjects=[x.text.strip() for x in b.find_all(attrs={"class":"subject"})]
    images=[x["src"] for x in b.find_all(attrs={"class":"img-responsive"})]
    return {
        "faculties":faculties,
        "subjects":subjects,
        "images":images,
    }

def exam_schedule():
    a=r.get('https://student.amizone.net/Examination/ExamSchedule?X-Requested-With=XMLHttpRequest')
    b = bs4.BeautifulSoup(a.content, 'html.parser')
    courseCode = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Code"})]
    courseTitle = [c.text.strip() for c in b.find_all(attrs={'data-title': "Course Title"})]
    ExamDate = [c.text.strip() for c in b.find_all(attrs={'data-title': "Exam Date"})]
    Time = [c.text.strip() for c in b.find_all(attrs={'data-title': "Time"})]
    return {
        "courseCode": courseCode,
        "courseTitle": courseTitle,
        "ExamDate": ExamDate,
        "Time":Time,
    }

def timetable():
    a=r.get("https://student.amizone.net/TimeTable/Home?X-Requested-With=XMLHttpRequest")
    b = bs4.BeautifulSoup(a.content, 'html.parser')

    # get timetable from active pane
    # b=b.find(attrs={"class":"tab-pane"})
    # get timetable of current day
    b=b.find(attrs={'id':date.today().strftime("%A")})
    # any of these will work
    if b is None:
        courseCode = []
        courseTeacher = []
        classLocation = []
        Time = []
    else:
        courseCode = [x.text.strip() for x in b.find_all(attrs={"class":"course-code"})]
        courseTeacher = [c.text.strip() for c in b.find_all(attrs={'class': "course-teacher"})]
        classLocation = [x.text.strip() for x in b.find_all(attrs={"class":"class-loc"})]
        Time = [x.text.strip() for x in b.find_all(attrs={"class": "class-time"})]
    
    return {
        "courseCode": courseCode,
        "courseTeacher": courseTeacher,
        "classLocation": classLocation,
        "Time":Time,
    }

app = Flask(__name__)

@app.route('/',methods=['GET'])
def test():
    return "<body bgcolor='rebeccapurple' style='color:white'></body>"\
            "<h2><pre>Hello World!</pre></h2>" \
            "<pre>Welcome to Amizone rest API!</pre>" \
            "<br>" \
            "<pre>While You are here, You might want to learn about the API Paths:</pre>" \
            "<pre><mark style='background-color:dodgerblue;'>GET</mark><pre>" \
            "<pre>https://amizone-api.herokuapp.com/          : Will get you here</pre>" \
            "<br>" \
            "<pre><mark style='background-color:springgreen;'>POST</mark></pre>" \
            "<p>Form data:</p>" \
            "<pre>username=amizone_username</pre>" \
            "<pre>password=amizone_password</pre>" \
            "<br>" \
            "<pre>https://amizone-api.herokuapp.com/login     : To validate username and Password</pre>" \
            "<pre>https://amizone-api.herokuapp.com/profile   : To get User's Profile</pre>"\
            "<pre>https://amizone-api.herokuapp.com/timetable : To get Current timetable</pre>" \
            "<pre>https://amizone-api.herokuapp.com/courses   : To get Courses information</pre>" \
            "<pre>https://amizone-api.herokuapp.com/faculty   : To get Faculties details</pre>" \
            "<pre>https://amizone-api.herokuapp.com/schedule  : To get Exam Schedule</pre>" \
            "<pre>https://amizone-api.herokuapp.com/results   : To get Latest Exam resulta</pre>" \
            "<br>" \
            "<pre align='center'>© All Rights Reserved Akshansh Kumar</pre>"

@app.route('/login',methods=['POST'])
def log():
    return login(request.form['username'],request.form['password'])

@app.route('/profile',methods=['POST'])
def profile():
    login(request.form['username'], request.form['password'])
    return my_profile(request.form['username'])

@app.route('/courses',methods=['POST'])
def courses():
    login(request.form['username'], request.form['password'])
    return my_courses()

@app.route('/faculty',methods=['POST'])
def faculty():
    login(request.form['username'], request.form['password'])
    return my_faculty()

@app.route('/schedule',methods=['POST'])
def schedule():
    login(request.form['username'], request.form['password'])
    return exam_schedule()

@app.route('/results',methods=['POST'])
def result():
    login(request.form['username'], request.form['password'])
    return results()

@app.route('/timetable',methods=['POST'])
def time():
    login(request.form['username'], request.form['password'])
    return timetable()

if __name__ == "__main__":
    app.run()
