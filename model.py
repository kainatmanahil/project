


class student_login(db.Model):
    __tablename__ = 'student_login'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    student_username = db.Column(db.String(100))
    student_password = db.Column(db.Integer)
    student_cnic = db.Column(db.String(100))
    student_department = db.Column(db.String(100))
    student_session = db.Column(db.String(100))
    date_created = db.Column(db.DATE, default=datetime.now())