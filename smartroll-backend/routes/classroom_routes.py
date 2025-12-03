from flask import Blueprint, request, jsonify
from models import db, ApprovedSubnet
from datetime import datetime
import os
from utils.ip_utils import get_ip_prefix

# Initialize the blueprint
classroom_bp = Blueprint("classroom_bp", __name__, url_prefix="/classroom")

# Instructor-only: Add a new classroom network
@classroom_bp.route("/add", methods=["POST"])
def add_classroom():
    # Get API key from request header
    api_key = request.headers.get('x-api-key')

    # Validate admin key (from .env)
    if api_key != os.getenv('ADMIN_API_KEY'):
        return jsonify({"error": "Unauthorized. Invalid or missing API key."}), 403

    # Get the network prefix of the instructor's Wi-Fi
    prefix = get_ip_prefix()

    # Check if this prefix already exists in database
    existing = ApprovedSubnet.query.filter_by(prefix=prefix).first()
    if existing:
        return jsonify({"message": "This subnet is already registered"}), 200

    # Save to the database
    new_classroom = ApprovedSubnet(
        prefix=prefix,
        created_by="admin",
        created_at=datetime.utcnow()
    )
    db.session.add(new_classroom)
    db.session.commit()

    return jsonify({"message": "Classroom added", "prefix": prefix}), 201


# List all approved classrooms
@classroom_bp.route("/list", methods=["GET"])
def list_classrooms():
    subnets = ApprovedSubnet.query.all()
    return jsonify([s.prefix for s in subnets])
