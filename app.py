from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

db = SQLAlchemy()
# from model import *


UPLOAD_FOLDER = '/home/rajpoot/Documents/mini project/hamza/sanooo/pdf files'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:RajaHamza@localhost:3306/assignment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)




class Student_login(db.Model):
    # __tablename__ = "student_login"
    id = db.Column(db.Integer, primary_key=True)
    
    student_username   = db.Column(db.String(100), nullable=False)
    student_password   = db.Column(db.String(100), nullable=False)
    student_department = db.Column(db.String(100), nullable=False)
    student_session    = db.Column(db.String(100), nullable=False)
    student_cnic       = db.Column(db.Integer, nullable=False)
    date_created       = db.Column(db.DATE, default=datetime.now())

class Teachers_login(db.Model):
    __tablename__    = "teachers_login"
    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(100))
    teacher_password = db.Column(db.String(100), nullable=False)
    date_created     = db.Column(db.DATE, default=datetime.now())

class Courses(db.Model):

    id     = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100))

class Program(db.Model):

    id      = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(100))

class Sessions(db.Model):

    id      = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(100))

class Student_Submit(db.Model):
    __tablename__="student_submit"
    id      = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100))
    program = db.Column(db.String(100))
    session = db.Column(db.String(100))
    assignment_name = db.Column(db.String(100), nullable=True)
    obtain_marks = db.Column(db.String(100), nullable=True)

class Add_assignment(db.Model):

    __tablename__ = "assignment"

    id            = db.Column(db.Integer, primary_key=True)
    topic         = db.Column(db.String(100))
    question      = db.Column(db.String(100))
    number        = db.Column(db.Integer)
    deadline      = db.Column(db.String(100))
    created       = db.Column(db.DATE, default=datetime.now())
    course        = db.Column(db.String(100))
    teacher       = db.Column(db.String(100))
    program       = db.Column(db.String(100))
    session       = db.Column(db.String(100))
    obtain_marks       = db.Column(db.String(100))
    student_name       = db.Column(db.String(100))




@app.route("/")
def home():
    if session.get('username'):
        return render_template("home.html")
    else:
        return render_template("index.html")
    

@app.route("/register", methods=['GET','POST'])
def register():

    se = Sessions.query.all()
    pr = Program.query.all()

    if request.method == 'POST':
        student_cnic = request.form.get('CNIC')
        student_username = request.form.get('username')
        student_password = request.form.get('password')
        student_department = request.form.get('program')
        student_session = request.form.get('session')

        user = Student_login.query.filter_by(student_username=student_username).first()
    
        if not user:
            add = Student_login(student_department=student_department,student_session=student_session,student_username = student_username, student_password = student_password,student_cnic = student_cnic)
            db.session.add(add)
            db.session.commit()
    
            return redirect('/')
    else:
        return render_template("register.html",se=se,pr=pr)

    

@app.route('/login', methods=['GET', 'POST'])
def login():
   
    if request.method == 'POST':
        identity=request.form.get("identity")
        if  identity == "student":

            username = request.form.get("username")
            password = request.form.get("password")
            
            user_student = Student_login.query.filter_by(student_username=username , student_password=password).first()
            
            if user_student:
                session["username"] = user_student.student_username
               
                return redirect("/")
         
        elif identity == "teacher":

            username = request.form.get("username")
            password = request.form.get("password")
            user_teacher = Teachers_login.query.filter_by(name=username, teacher_password=password).first()
            
            if user_teacher:
                session["name"] = user_teacher.name
                return redirect("/dashboad")
    return render_template("index.html")
@app.route("/logout")
def logout():
    session['username'] = []
    session['name'] = []
    flash(" You are logged out successfully")
    return redirect('/')

@app.route("/dashboad")
def teacher():
    if session.get('name'):
        return render_template("master_template.html")
    else :
        return render_template("index.html")

@app.route("/add_assignment",, methods=['GET','POST'])
def add_assignment():
    

    if request.method =='POST':

        subject = request.form.get('subject')
        sesion = request.form.get('session')
        program = request.form.get('program')
        topic = request.form.get('topic')
        number = request.form.get('number')
        question = request.form.get('question')
        deadline = request.form.get('deadline')

        teacher =session["name"]
        add = Add_assignment(teacher=teacher,course=subject,session=sesion,program=program,topic=topic,number=number,question=question,deadline=deadline)
        db.session.add(add)
        db.session.commit()
        return redirect("/ab")



@app.route("/view_assignment_student")
def view_assignment_student():

    openn = Add_assignment.query.all() 
    user = session["username"]
    st = Student_login.query.filter(Student_login.student_username==user).first()

    return render_template("view_assignment_student.html",st=st,openn=openn)

@app.route("/view_assignment")
def view_assignment():

    openn = Add_assignment.query.all() 

    return render_template("view_assignment.html",openn=openn)

@app.route("/submitted_assignment/<name>",  methods=['GET','POST'])
def sta(name):
    st = Student_Submit.query.all()
    
    update = Student_Submit.query.filter_by(student_id=name).first()
    
    if request.method == 'POST':
    
        update.obtain_marks = request.form.get("marks")
        
        db.session.commit()
    
        return redirect("/submitted_assignment")
      

        
    return render_template("submitted_assignment.html",st=st)


@app.route("/submitted_assignment",  methods=['GET','POST'])
def submitted_assignment():
    
    st = Student_Submit.query.all()
    
    
    return render_template("submitted_assignment.html",st=st)

@app.route("/view_assignment_result")
def view_assignment_result():
    
    openn = Add_assignment.query.all() 
    name = session["username"]
    rs = Student_Submit.query.filter_by(student_id=name).first()

    return render_template("view_assignment_result.html",rs=rs,openn=openn)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/savedata/<int:id>",methods=['GET','POST'])
def savedata(id):


    user = Student_login.query.filter(Student_login.id==id).first()


    if request.method == 'POST':    

        # check if the post request has the file part
        if 'file' not in request.files:

            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            st = Student_Submit(student_id=user.student_username,session=user.student_session,program=user.student_department)
            db.session.add(st)
            db.session.commit()
            return redirect("/view_assignment_student")

    return render_template("view_assignment_student.html")


@app.route("/update_assignment/<int:id>", methods=['GET','POST'])
def update_assignment(id):    

    update = Add_assignment.query.get(id)
    course = Courses.query.all()
    session = Sessions.query.all()
    program = Program.query.all()


    if request.method =='POST':

        update.subject = request.form.get('subject')
        update.sesion = request.form.get('session')
        update.program = request.form.get('program')
        update.topic = request.form.get('topic')
        update.number = request.form.get('number')
        update.question = request.form.get('question')
        update.deadline = request.form.get('deadline')

        try:
            
            db.session.commit()
            return redirect("/view_assignment")
        except:
            return "There was a problem to update"


    return render_template("update_template.html", session=session,course=course,program=program,update=update)


@app.route("/delete_assignment/<int:id>", methods=['GET','POST'])
def delete_assignment(id):

    delete = Add_assignment.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect("/view_assignment")



@app.route("/ab", methods=['GET', 'POST'])
def assignment():


    course = Courses.query.all()
    session = Sessions.query.all()
    program = Program.query.all()

    return render_template("assignment.html",session=session,course=course,program=program)
    

if __name__ == "__main__":
    app.run(debug=True,port = 6002)