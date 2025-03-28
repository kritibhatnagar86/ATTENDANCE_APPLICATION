import React, { useState, useEffect } from "react";
import axios from "axios";
import { DeviceUUID } from "device-uuid";

const App = () => {
  const [studentId, setStudentId] = useState("");
  const [name, setName] = useState("");
  const [location, setLocation] = useState(null);
  const [attendance, setAttendance] = useState([]);
  const [totalStudents, setTotalStudents] = useState(0); // Added state for total students
  const [loading, setLoading] = useState(false);
  const [deviceId, setDeviceId] = useState("");

  useEffect(() => {
    const uuid = new DeviceUUID().get();
    setDeviceId(uuid);
    fetchAttendance();
  }, []);

  const fetchAttendance = async () => {
    try {
      const response = await axios.get("http://localhost:5000/attendance");
      setAttendance(response.data.students); // Access students array
      setTotalStudents(response.data.total_present); // Store total student count
    } catch (error) {
      console.error("Error fetching attendance:", error);
    }
  };

  const handleCheckIn = async () => {
    if (!studentId || !name) {
      alert("Please enter all fields.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const latitude = pos.coords.latitude;
        const longitude = pos.coords.longitude;

        try {
          setLoading(true);

          const response = await axios.post("http://localhost:5000/student_checkin", {
            student_id: studentId,
            name,
            latitude,
            longitude,
            device_id: deviceId,
          });

          if (response.data.warning) {
            alert(response.data.warning);
          } else {
            alert("Check-in successful!");
          }

          setLoading(false);
          fetchAttendance();
        } catch (error) {
          setLoading(false);
          console.error("Error checking in:", error);
          alert("Error checking in. Please try again.");
        }
      },
      (err) => {
        console.error("Error getting location:", err);
        alert("Location access is required for check-in.");
      }
    );
  };

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (pos) => setLocation({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
      (err) => console.error("Error getting location:", err)
    );
  }, []);

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h1 className="text-xl font-bold">Student Check-in</h1>

      <input
        className="border p-2 w-full"
        type="text"
        placeholder="Student ID"
        value={studentId}
        onChange={(e) => setStudentId(e.target.value)}
      />

      <input
        className="border p-2 w-full"
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <button
        className={`bg-blue-500 text-white px-4 py-2 rounded ${loading ? "opacity-50" : ""}`}
        onClick={handleCheckIn}
        disabled={loading}
      >
        {loading ? "Processing..." : "Check-in"}
      </button>

      <h2 className="text-lg font-bold mt-4">Today's Attendance</h2>

      <p className="text-gray-700 font-semibold">Total Students: {totalStudents}</p>

      {attendance.length > 0 ? (
        <ul className="border p-2 rounded">
          {attendance.map((record, index) => (
            <li key={index} className="border-b p-2">
              <strong>{record.name}</strong> - {record.student_id} <br />
              <span className="text-gray-500 text-sm">{record.date}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">No attendance records yet.</p>
      )}
    </div>
  );
};

export default App;
