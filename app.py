# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, date
# from flask_cors import CORS
# from sqlalchemy import and_
# from dotenv import load_dotenv
# import os

# from math import radians, sin, cos, sqrt, atan2

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# # Database Configuration
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # Initialize database
# db = SQLAlchemy(app)

# # Define Database Models
# class Student(db.Model):
#     __tablename__ = "students"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     student_id = db.Column(db.String(50), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     device_id = db.Column(db.String(100))
#     date = db.Column(db.Date, default=date.today)

# class Attendance(db.Model):
#     __tablename__ = "attendance"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     student_id = db.Column(db.String(50), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     date = db.Column(db.Date, default=date.today)

# # Haversine formula to calculate distance
# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371  # Radius of Earth in km
#     lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

#     dlat = lat2 - lat1
#     dlon = lon2 - lon1

#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))

#     return R * c  # Distance in km

# # Route: API Health Check
# @app.route("/")
# def home():
#     return "Flask app connected to NeonDB!"
# @app.route("/student_checkin", methods=["POST"])
# def student_checkin():
#     try:
#         data = request.json
#         print("Received Data:", data)  # Debugging incoming data

#         required_fields = ["student_id", "name", "latitude", "longitude", "device_id"]
#         if not all(key in data for key in required_fields):
#             print("Error: Missing required fields")
#             return jsonify({"error": "Missing required fields"}), 400

#         # Check if student has already checked in today
#         print("Checking if student has already checked in...")
#         student_check = Student.query.filter(and_(
#             Student.student_id == data["student_id"],
#             Student.date == date.today()
#         )).first()
        
#         if student_check:
#             print("Student already checked in.")
#             return jsonify({"warning": "This student ID has already checked in today."}), 200

#         # Check if device has already been used for check-in today
#         print("Checking if device has already been used for check-in...")
#         device_check = Student.query.filter(and_(
#             Student.device_id == data["device_id"],
#             Student.date == date.today()
#         )).first()
        
#         if device_check:
#             print("Device already checked in.")
#             return jsonify({"warning": "This device has already been used for check-in today."}), 200

#         # Insert new check-in record
#         print("Inserting new student check-in record...")
#         new_student = Student(
#             student_id=data["student_id"],
#             name=data["name"],
#             latitude=float(data["latitude"]),
#             longitude=float(data["longitude"]),
#             device_id=data["device_id"]
#         )

#         db.session.add(new_student)
#         db.session.commit()

#         print("Student check-in successful!")
#         return jsonify({"message": "Student check-in successful!"}), 201

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error in student_checkin: {e}")  # Print actual error in console
#         return jsonify({"error": str(e)}), 500

# # Route: Mark Attendance
# @app.route("/mark_attendance", methods=["POST"])
# def mark_attendance():
#     try:
#         data = request.json
#         print("Received Data:", data)  # Debugging

#         if not data or "classroom_lat" not in data or "classroom_long" not in data:
#             return jsonify({"error": "Missing required fields"}), 400

#         classroom_lat = float(data["classroom_lat"])
#         classroom_long = float(data["classroom_long"])
#         radius_km = float(data.get("radius", 0.1))  # Default ~100m

#         today_students = Student.query.filter(Student.date == date.today()).all()
#         print(f"Total students checked in today: {len(today_students)}")

#         if not today_students:
#             return jsonify({"warning": "No students have checked in today."}), 200

#         present_students = []

#         for student in today_students:
#             print(f"Checking Student {student.student_id} at ({student.latitude}, {student.longitude})")

#             distance = haversine(student.latitude, student.longitude, classroom_lat, classroom_long)
#             print(f"Student: {student.student_id}, Distance: {distance} km")  # Debugging

#             if distance <= radius_km:
#                 existing_attendance = Attendance.query.filter(
#                     Attendance.student_id == student.student_id,
#                     Attendance.date == date.today()
#                 ).first()

#                 if not existing_attendance:
#                     new_attendance = Attendance(student_id=student.student_id, name=student.name)
#                     db.session.add(new_attendance)
#                     present_students.append(new_attendance)
#                     print(f"Marked Present: {student.student_id}")

#         if present_students:
#             print(f"Committing attendance for {len(present_students)} students")
#             db.session.commit()
#             return jsonify({
#                 "message": "Attendance marked successfully",
#                 "present_count": len(present_students)
#             }), 201
#         else:
#             return jsonify({"warning": "No new students within the attendance zone or already marked."}), 200

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error in mark_attendance: {str(e)}")
#         return jsonify({"error": str(e)}), 500



# # Route: Get Attendance Records
# @app.route("/attendance", methods=["GET"])
# def get_attendance():
#     records = Attendance.query.filter(Attendance.date == date.today()).all()
#     total_students = len(records)  # Count total students present today

#     return jsonify({
#         "total_present": total_students,
#         "students": [
#             {"student_id": rec.student_id, "name": rec.name, "date": rec.date.strftime("%Y-%m-%d")}
#             for rec in records
#         ]
#     })

# # Initialize Database
# with app.app_context():
#     db.create_all()

# # Run Flask App
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)



from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from flask_cors import CORS
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
import os
from math import radians, sin, cos, sqrt, atan2
from dotenv import load_dotenv
from datetime import datetime, UTC,timezone
# Student Check-in Route
from datetime import timedelta
from sqlalchemy import and_


from sqlalchemy import text


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# -------------------- Database Models --------------------

# Student Model
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    device_id = db.Column(db.String(100))
    date = db.Column(db.Date, default=date.today)

# Attendance Model
class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=date.today)

# Admin Credentials Model
class Admin(db.Model):
    __tablename__ = "admin_credentials"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)  # Hashed password

# Admin Location Model
class AdminLocation(db.Model):
    __tablename__ = "admin_location"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     # Add admin_id if needed
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(datetime.UTC))  # Fix UTC issue
     


# -------------------- Helper Functions --------------------

# Haversine formula to calculate distance in km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Distance in km

# -------------------- Routes --------------------

# API Health Check
@app.route("/")
def home():
    return "Flask app connected to NeonDB!"

# Admin Login Route
@app.route("/admin_login", methods=["POST"])
def admin_login():
    try:
        data = request.json
        admin = Admin.query.filter_by(admin_id=data["admin_id"]).first()

        if admin and check_password_hash(admin.password, data["password"]):
            return jsonify({"message": "Admin login successful!"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Store Admin Location

print(f"📌 Connected to database: {app.config['SQLALCHEMY_DATABASE_URI']}")





# with app.app_context():  # ✅ Fix: Wrap in application context
#     try:
#         query = text("INSERT INTO admin_location (latitude, longitude, timestamp) VALUES (26.9156, 75.7825, NOW());")
#         db.session.execute(query)
#         db.session.commit()
#         print("✅ Manual insert successful!")
#     except Exception as e:
#         print(f"❌ Error inserting manually: {e}")




@app.route("/admin_location", methods=["POST"])
def save_admin_location():
    try:
        data = request.json
        print("🔹 Received Data:", data)  # Debugging

        # Check if required fields exist
        if "latitude" not in data or "longitude" not in data:
            print("❌ Missing latitude or longitude")
            return jsonify({"error": "Missing required fields"}), 400

        new_location = AdminLocation(
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            timestamp=datetime.now(UTC)  # ✅ Fix datetime issue
        )

        db.session.add(new_location)
        db.session.flush()  
        db.session.commit()

        print("✅ Admin location inserted successfully!")
        return jsonify({"message": "Admin location stored!"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error inserting admin location: {e}")  # Print error to console
        return jsonify({"error": str(e)}), 500




@app.route("/student_checkin", methods=["POST"])
def student_checkin():
    try:
        data = request.json
        print(f"📌 Received Student Data: {data}")

        # Get latest admin location
        latest_admin_location = AdminLocation.query.order_by(AdminLocation.timestamp.desc()).first()
        if not latest_admin_location:
            print("❌ No admin location found")
            return jsonify({"error": "No admin location found"}), 400

        print(f"📍 Latest Admin Location: {latest_admin_location.latitude}, {latest_admin_location.longitude}, {latest_admin_location.timestamp}")

        # Convert latest admin timestamp to UTC-aware
        if latest_admin_location.timestamp.tzinfo is None:
            admin_timestamp = latest_admin_location.timestamp.replace(tzinfo=timezone.utc)  # ✅ Fix here
        else:
            admin_timestamp = latest_admin_location.timestamp

        now_utc = datetime.now(timezone.utc)  # ✅ Fix timezone issue
        time_difference = (now_utc - admin_timestamp).total_seconds()

        print(f"🕒 Current Time: {now_utc}")
        print(f"⏳ Time Difference: {time_difference} seconds")

        if time_difference > 300:  # 5 minutes
            print("❌ Admin location is too old")
            return jsonify({"warning": "Admin location is older than 5 minutes"}), 400

        # Check student's distance from admin's last location
        student_lat, student_long = float(data["latitude"]), float(data["longitude"])
        distance = haversine(student_lat, student_long, latest_admin_location.latitude, latest_admin_location.longitude)

        print(f"📏 Student Distance from Admin: {distance} km")

        if distance > 0.5:  # 500m radius
            print("❌ Student is too far from admin")
            return jsonify({"warning": "You are not within the valid check-in area"}), 400

        # Check if student has already checked in today
        student_check = Student.query.filter(and_(
            Student.student_id == data["student_id"],
            Student.date == datetime.now(UTC).date()
        )).first()

        print(f"📌 Student Check-in Status: {student_check}")

        if student_check:
            print("⚠️ Student has already checked in today")
            return jsonify({"warning": "This student ID has already checked in today."}), 200

        # Check if device has already been used for check-in today
        device_check = Student.query.filter(and_(
            Student.device_id == data["device_id"],
            Student.date == datetime.now(UTC).date()
        )).first()

        print(f"📌 Device Check-in Status: {device_check}")

        if device_check:
            print("⚠️ This device has already been used for check-in today")
            return jsonify({"warning": "This device has already been used for check-in today."}), 200

        # Insert new student record
        new_student = Student(
            student_id=data["student_id"],
            name=data["name"],
            latitude=student_lat,
            longitude=student_long,
            device_id=data["device_id"],
            date=datetime.now(UTC).date()
        )

        db.session.add(new_student)
        db.session.commit()

        print("✅ Student check-in successful!")
        return jsonify({"message": "Student check-in successful!"}), 201

    except Exception as e:
        print(f"❌ Error in student check-in: {e}")
        return jsonify({"error": str(e)}), 500

# Get Attendance Records
@app.route("/attendance", methods=["GET"])
def get_attendance():
    records = Attendance.query.filter(Attendance.date == date.today()).all()
    total_students = len(records)

    return jsonify({
        "total_present": total_students,
        "students": [
            {"student_id": rec.student_id, "name": rec.name, "date": rec.date.strftime("%Y-%m-%d")}
            for rec in records
        ]
    })



with app.app_context():
    result = db.session.execute(text("SELECT * FROM admin_location")).fetchall()
    print("📌 Admin Locations:", result)
# Initialize Database
with app.app_context():
    db.create_all()

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True, port=5000)

