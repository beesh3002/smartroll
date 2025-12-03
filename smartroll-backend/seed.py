from app import create_app
from models import db, Instructor, Student, Course, Enrollment

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    inst = Instructor(name="Dr. Test", email="test@uosh.ae", password_hash="dev")
    db.session.add(inst)

    c1 = Course(code="CS101", name="Intro to CS", instructor_id=1)
    db.session.add(c1)

    s1 = Student(name="Alice", student_id="U22100001", mac_address="AA:BB:CC:DD:EE:01")
    s2 = Student(name="Bob",   student_id="U22100002", mac_address="AA:BB:CC:DD:EE:02")
    db.session.add_all([s1, s2])
    db.session.flush()

    db.session.add_all([
        Enrollment(course_id=c1.id, student_id=s1.id),
        Enrollment(course_id=c1.id, student_id=s2.id),
    ])

    db.session.commit()
    print("Seed complete.")
