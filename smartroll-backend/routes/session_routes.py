from flask import Blueprint, request, jsonify
from models import db, Course, Session
from routes.auth_routes import require_admin_key

session_bp = Blueprint("sessions", __name__, url_prefix="/sessions")

# =====================================================
# START SESSION (Admin only)
# =====================================================
@session_bp.route("/start", methods=["POST"])
def start_session():
    if not require_admin_key():
        return jsonify({"error":"unauthorized"}), 401
    data = request.get_json() or {}
    course_id = data.get("course_id")
    min_presence = data.get("min_presence_minutes", 30)
    heartbeat = data.get("heartbeat_minutes", 10)
    grace = data.get("grace_minutes", 5)

    s = Session(course_id=course_id, min_presence_minutes=min_presence,
                heartbeat_minutes=heartbeat, grace_minutes=grace)
    db.session.add(s)
    db.session.commit()
    return jsonify({"message":"session_started","session_id": s.id})

# =====================================================
# END SESSION (Admin only)
# =====================================================
@session_bp.route("/end", methods=["POST"])
def end_session():
    if not require_admin_key():
        return jsonify({"error":"unauthorized"}), 401
    data = request.get_json() or {}
    session_id = data.get("session_id")
    s = Session.query.get(session_id)
    if not s:
        return jsonify({"error":"not_found"}), 404
    from datetime import datetime
    s.end_time = datetime.utcnow()
    db.session.commit()
    return jsonify({"message":"session_ended","session_id": s.id})

# =====================================================
# GET SESSION DETAILS (Public - for students)
# =====================================================
@session_bp.route("/<int:session_id>", methods=["GET"])
def get_session(session_id):
    """Get session details including heartbeat_minutes. Accessible to students."""
    s = Session.query.get(session_id)
    if not s:
        return jsonify({"error": "session_not_found"}), 404
    
    return jsonify({
        "id": s.id,
        "course_id": s.course_id,
        "start_time": s.start_time.isoformat() if s.start_time else None,
        "end_time": s.end_time.isoformat() if s.end_time else None,
        "min_presence_minutes": s.min_presence_minutes,
        "heartbeat_minutes": s.heartbeat_minutes,
        "grace_minutes": s.grace_minutes
    }), 200
