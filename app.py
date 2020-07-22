import requests
import bs4
from flask import Flask,request

URL         = "https://student.amizone.net/"
URL_LOGIN   = "https://student.amizone.net/Login/Login"
URL_HOME    = "https://student.amizone.net/Home"

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
        logged = s.post(URL_LOGIN,data=data)
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
            percentage.append(100.0)
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
    return "Hello World"

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