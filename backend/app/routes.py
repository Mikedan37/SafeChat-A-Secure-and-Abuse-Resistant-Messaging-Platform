import pyotp
import uuid

from bcrypt import checkpw
from flask import Blueprint, render_template, request, jsonify, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import socketio
from .models import User, Message, Notification, BlockedUser
from .utils.helpers import files
from .generate_reset_token import generate_reset_token, verify_reset_token

# Define the main blueprint
main = Blueprint('main', __name__)

# =======================
# User Management Routes
# =======================

@main.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user.is_admin:
        return jsonify({"msg": "Unauthorized"}), 403
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)

@main.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing email, password, or name"}), 400

    # Proceed with creating a new user
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Registration successful"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "user": {"id": user.id, "username": user.username}}), 200

    return jsonify({"error": "Invalid email or password"}), 401

@main.route("/delete_user", methods=["DELETE"])
@jwt_required()
def delete_user():
    data = request.get_json()
    password = data.get('password')

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not user.check_password(password):
        return jsonify({"msg": "Incorrect password"}), 403

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"}), 200


@main.route("/profile", methods=["GET", "PUT"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if request.method == "GET":
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }), 200

    if request.method == "PUT":
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({"msg": "Profile updated"}), 200


# =====================
# Two-Factor Authentication
# =====================

@main.route("/enable_2fa", methods=["POST"])
@jwt_required()
def enable_2fa():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32()
        db.session.commit()

    otp = pyotp.TOTP(user.mfa_secret)
    qr_code_url = otp.provisioning_uri(name=user.email, issuer_name="SafeChat")

    return jsonify({"qr_code_url": qr_code_url}), 200


# =======================
# Password Reset
# =======================

@main.route("/request_reset", methods=["POST"])
def request_password_reset():
    data = request.form
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    token = generate_reset_token(email)
    reset_url = url_for('main.reset_password', token=token, _external=True)

    print(f"Password reset link: {reset_url}")

    return jsonify({"msg": "Password reset email sent"}), 200


@main.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        return jsonify({"msg": "Invalid or expired token"}), 400

    if request.method == "POST":
        new_password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"msg": "User not found"}), 404

        user.set_password(new_password)
        db.session.commit()

        return jsonify({"msg": "Password reset successful"}), 200

    return render_template("reset_password.html", token=token)


# =======================
# Messaging Routes
# =======================

@main.route("/send_message", methods=["POST"])
@jwt_required()
def send_message():
    sender_id = get_jwt_identity()
    data = request.form
    receiver_id = data.get('receiver_id')
    content = data.get('content', "")
    file = request.files.get('file')

    if not receiver_id or not (content or file):
        return jsonify({"msg": "Missing fields"}), 400

    thread_id = data.get('thread_id', str(uuid.uuid4()))

    file_url = None
    if file:
        filename = files.save(file)
        file_url = f"/static/uploads/{filename}"

    message = Message(thread_id=thread_id, sender_id=sender_id, receiver_id=receiver_id, content=content, file_url=file_url)
    db.session.add(message)
    db.session.commit()

    return jsonify({"msg": "Message sent!", "thread_id": thread_id}), 201


@main.route("/get_thread/<string:thread_id>", methods=["GET"])
@jwt_required()
def get_thread(thread_id):
    messages = Message.query.filter_by(thread_id=thread_id).order_by(Message.timestamp).all()
    if not messages:
        return jsonify({"msg": "No messages found"}), 404

    thread = [{"sender": m.sender_id, "content": m.content, "timestamp": m.timestamp} for m in messages]
    return jsonify({"thread": thread}), 200


# =======================
# Notification Routes
# =======================

@main.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()

    results = [{"id": n.id, "content": n.content} for n in notifications]
    return jsonify({"notifications": results}), 200


@main.route("/notifications/read", methods=["POST"])
@jwt_required()
def mark_notifications_read():
    user_id = get_jwt_identity()
    Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})
    db.session.commit()
    return jsonify({"msg": "Notifications marked as read"}), 200


# =======================
# Admin Routes
# =======================

@main.route("/admin/users", methods=["GET"])
@jwt_required()
def get_all_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_admin:
        return jsonify({"msg": "Access denied"}), 403

    users = User.query.all()
    result = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    return jsonify({"users": result}), 200


# =======================
# Socket.IO
# =======================

@socketio.on("send_message")
def handle_send_message(data):
    thread_id = data["thread_id"]
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    content = data["content"]

    message = Message(thread_id=thread_id, sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()

    socketio.emit("receive_message", {
        "thread_id": thread_id,
        "sender_id": sender_id,
        "content": content,
    }, room=receiver_id)


# =======================
# Test Routes
# =======================

import pytest
from . import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"SafeChat App is Running!"


# =======================
# Miscellaneous Routes
# =======================

@main.route("/")
def home():
    return "SafeChat App is Running!"