import uuid
from models import db, Student
from flask import Blueprint, request, jsonify, current_app

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def require_admin_key():
    key = request.headers.get("X-API-Key")
    return key and key == current_app.config["ADMIN_API_KEY"]

@auth_bp.route("/ping")
def ping():
    return jsonify({"ok": True})

@auth_bp.route("/register_device", methods=["POST"])
def register_device():
    data = request.get_json() or {}
    student_id = data.get("student_id")

    print(data)
    if not student_id:
        return jsonify({"error": "student_id required"}), 400

    # Create a unique device token (UUID4)
    device_token = str(uuid.uuid4())

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student.device_token = device_token
    db.session.commit()

    return jsonify({"device_token": device_token})
