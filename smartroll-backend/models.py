from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# People
class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256))  # you can hash later

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    student_id = db.Column(db.String(32), unique=True, index=True)
    mac_address = db.Column(db.String(32), unique=True, index=True)

# Courses & enrollment
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), index=True)
    name = db.Column(db.String(120))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

# Class sessions
class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    min_presence_minutes = db.Column(db.Integer, default=30)
    heartbeat_minutes = db.Column(db.Integer, default=10)
    grace_minutes = db.Column(db.Integer, default=5)

# Attendance logs (events)
class AttendanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    mac = db.Column(db.String(32))
    status = db.Column(db.String(16))  # Present/Late/Left/Absent/Heartbeat
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


#This table stores the IP prefix for each approved classroom network
class ApprovedSubnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(32), unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
