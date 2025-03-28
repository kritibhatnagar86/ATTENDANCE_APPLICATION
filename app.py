from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_cors import CORS
from sqlalchemy import and_
from dotenv import load_dotenv
import os

from math import radians, sin, cos, sqrt, atan2

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Define Database Models
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

class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=date.today)

# Haversine formula to calculate distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Distance in km

# Route: API Health Check
@app.route("/")
def home():
    return "Flask app connected to NeonDB!"
@app.route("/student_checkin", methods=["POST"])
def student_checkin():
    try:
        data = request.json
        print("Received Data:", data)  # Debugging incoming data

        required_fields = ["student_id", "name", "latitude", "longitude", "device_id"]
        if not all(key in data for key in required_fields):
            print("Error: Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        # Check if student has already checked in today
        print("Checking if student has already checked in...")
        student_check = Student.query.filter(and_(
            Student.student_id == data["student_id"],
            Student.date == date.today()
        )).first()
        
        if student_check:
            print("Student already checked in.")
            return jsonify({"warning": "This student ID has already checked in today."}), 200

        # Check if device has already been used for check-in today
        print("Checking if device has already been used for check-in...")
        device_check = Student.query.filter(and_(
            Student.device_id == data["device_id"],
            Student.date == date.today()
        )).first()
        
        if device_check:
            print("Device already checked in.")
            return jsonify({"warning": "This device has already been used for check-in today."}), 200

        # Insert new check-in record
        print("Inserting new student check-in record...")
        new_student = Student(
            student_id=data["student_id"],
            name=data["name"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            device_id=data["device_id"]
        )

        db.session.add(new_student)
        db.session.commit()

        print("Student check-in successful!")
        return jsonify({"message": "Student check-in successful!"}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error in student_checkin: {e}")  # Print actual error in console
        return jsonify({"error": str(e)}), 500

# Route: Mark Attendance
@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    try:
        data = request.json
        print("Received Data:", data)  # Debugging

        if not data or "classroom_lat" not in data or "classroom_long" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        classroom_lat = float(data["classroom_lat"])
        classroom_long = float(data["classroom_long"])
        radius_km = float(data.get("radius", 0.1))  # Default ~100m

        today_students = Student.query.filter(Student.date == date.today()).all()
        print(f"Total students checked in today: {len(today_students)}")

        if not today_students:
            return jsonify({"warning": "No students have checked in today."}), 200

        present_students = []

        for student in today_students:
            print(f"Checking Student {student.student_id} at ({student.latitude}, {student.longitude})")

            distance = haversine(student.latitude, student.longitude, classroom_lat, classroom_long)
            print(f"Student: {student.student_id}, Distance: {distance} km")  # Debugging

            if distance <= radius_km:
                existing_attendance = Attendance.query.filter(
                    Attendance.student_id == student.student_id,
                    Attendance.date == date.today()
                ).first()

                if not existing_attendance:
                    new_attendance = Attendance(student_id=student.student_id, name=student.name)
                    db.session.add(new_attendance)
                    present_students.append(new_attendance)
                    print(f"Marked Present: {student.student_id}")

        if present_students:
            print(f"Committing attendance for {len(present_students)} students")
            db.session.commit()
            return jsonify({
                "message": "Attendance marked successfully",
                "present_count": len(present_students)
            }), 201
        else:
            return jsonify({"warning": "No new students within the attendance zone or already marked."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in mark_attendance: {str(e)}")
        return jsonify({"error": str(e)}), 500



# Route: Get Attendance Records
@app.route("/attendance", methods=["GET"])
def get_attendance():
    records = Attendance.query.filter(Attendance.date == date.today()).all()
    total_students = len(records)  # Count total students present today

    return jsonify({
        "total_present": total_students,
        "students": [
            {"student_id": rec.student_id, "name": rec.name, "date": rec.date.strftime("%Y-%m-%d")}
            for rec in records
        ]
    })

# Initialize Database
with app.app_context():
    db.create_all()

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True, port=5000)
