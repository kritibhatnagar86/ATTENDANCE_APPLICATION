// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import { DeviceUUID } from "device-uuid";

// const App = () => {
//   const [studentId, setStudentId] = useState("");
//   const [name, setName] = useState("");
//   const [location, setLocation] = useState(null);
//   const [attendance, setAttendance] = useState([]);
//   const [totalStudents, setTotalStudents] = useState(0); // Added state for total students
//   const [loading, setLoading] = useState(false);
//   const [deviceId, setDeviceId] = useState("");

//   useEffect(() => {
//     const uuid = new DeviceUUID().get();
//     setDeviceId(uuid);
//     fetchAttendance();
//   }, []);

//   const fetchAttendance = async () => {
//     try {
//       const response = await axios.get("http://localhost:5000/attendance");
//       setAttendance(response.data.students); // Access students array
//       setTotalStudents(response.data.total_present); // Store total student count
//     } catch (error) {
//       console.error("Error fetching attendance:", error);
//     }
//   };

//   const handleCheckIn = async () => {
//     if (!studentId || !name) {
//       alert("Please enter all fields.");
//       return;
//     }

//     navigator.geolocation.getCurrentPosition(
//       async (pos) => {
//         const latitude = pos.coords.latitude;
//         const longitude = pos.coords.longitude;

//         try {
//           setLoading(true);

//           const response = await axios.post("http://localhost:5000/student_checkin", {
//             student_id: studentId,
//             name,
//             latitude,
//             longitude,
//             device_id: deviceId,
//           });

//           if (response.data.warning) {
//             alert(response.data.warning);
//           } else {
//             alert("Check-in successful!");
//           }

//           setLoading(false);
//           fetchAttendance();
//         } catch (error) {
//           setLoading(false);
//           console.error("Error checking in:", error);
//           alert("Error checking in. Please try again.");
//         }
//       },
//       (err) => {
//         console.error("Error getting location:", err);
//         alert("Location access is required for check-in.");
//       }
//     );
//   };

//   useEffect(() => {
//     navigator.geolocation.getCurrentPosition(
//       (pos) => setLocation({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
//       (err) => console.error("Error getting location:", err)
//     );
//   }, []);

//   return (
//     <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4">
//       <h1 className="text-xl font-bold">Student Check-in</h1>

//       <input
//         className="border p-2 w-full"
//         type="text"
//         placeholder="Student ID"
//         value={studentId}
//         onChange={(e) => setStudentId(e.target.value)}
//       />

//       <input
//         className="border p-2 w-full"
//         type="text"
//         placeholder="Name"
//         value={name}
//         onChange={(e) => setName(e.target.value)}
//       />

//       <button
//         className={`bg-blue-500 text-white px-4 py-2 rounded ${loading ? "opacity-50" : ""}`}
//         onClick={handleCheckIn}
//         disabled={loading}
//       >
//         {loading ? "Processing..." : "Check-in"}
//       </button>

//       <h2 className="text-lg font-bold mt-4">Today's Attendance</h2>

//       <p className="text-gray-700 font-semibold">Total Students: {totalStudents}</p>

//       {attendance.length > 0 ? (
//         <ul className="border p-2 rounded">
//           {attendance.map((record, index) => (
//             <li key={index} className="border-b p-2">
//               <strong>{record.name}</strong> - {record.student_id} <br />
//               <span className="text-gray-500 text-sm">{record.date}</span>
//             </li>
//           ))}
//         </ul>
//       ) : (
//         <p className="text-gray-500">No attendance records yet.</p>
//       )}
//     </div>
//   );
// };

// export default App;




//latest comment




// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import FingerprintJS from "@fingerprintjs/fingerprintjs";

// const App = () => {
//   const [studentId, setStudentId] = useState("");
//   const [name, setName] = useState("");
//   const [location, setLocation] = useState(null);
//   const [attendance, setAttendance] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [deviceId, setDeviceId] = useState("");
//   const [totalStudents, setTotalStudents] = useState(0); 

//   useEffect(() => {
//     const getFingerprint = async () => {
//       const fp = await FingerprintJS.load();
//       const result = await fp.get();
//       setDeviceId(result.visitorId); // Unique device ID
//     };

//     getFingerprint();
//     fetchAttendance();
//   }, []);

//   const fetchAttendance = async () => {
//         try {
//           const response = await axios.get("http://localhost:5000/attendance");
//           setAttendance(response.data.students); // Access students array
//           setTotalStudents(response.data.total_present); // Store total student count
//         } catch (error) {
//           console.error("Error fetching attendance:", error);
//         }
//       };

//   const handleCheckIn = async () => {
//     if (!studentId || !name) {
//       alert("Please enter all fields.");
//       return;
//     }

//     navigator.geolocation.getCurrentPosition(
//       async (pos) => {
//         const latitude = pos.coords.latitude;
//         const longitude = pos.coords.longitude;

//         try {
//           setLoading(true);

//           const response = await axios.post("http://localhost:5000/student_checkin", {
//             student_id: studentId,
//             name,
//             latitude,
//             longitude,
//             device_id: deviceId, // Use the persistent device ID
//           });

//           if (response.data.warning) {
//             alert(response.data.warning);
//           } else {
//             alert("Check-in successful!");
//             handleMarkAttendance();
//           }

//           setLoading(false);
//           fetchAttendance();
//         } catch (error) {
//           setLoading(false);
//           console.error("Error checking in:", error);
//           alert("Error checking in. Please try again.");
//         }
//       },
//       (err) => {
//         console.error("Error getting location:", err);
//         alert("Location access is required for check-in.");
//       }
//     );
//   };

//   const handleMarkAttendance = async () => {
//     try {
//       setLoading(true);
//       await axios.post("http://localhost:5000/mark_attendance", {
//         classroom_lat: 26.865064775744624, // Example classroom coordinates
//         classroom_long: 75.81475703217994,
//         radius: 0.5,
//       });

//       alert("Attendance marked successfully!");
//       setLoading(false);
//       fetchAttendance();
//     } catch (error) {
//       setLoading(false);
//       console.error("Error marking attendance:", error);
//       alert("Error marking attendance. Please try again.");
//     }
//   };

//   useEffect(() => {
//     navigator.geolocation.getCurrentPosition(
//       (pos) => setLocation({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
//       (err) => console.error("Error getting location:", err)
//     );
//   }, []);

//   return (
//     <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4">
//       <h1 className="text-xl font-bold">Student Check-in</h1>

//       <input
//         className="border p-2 w-full"
//         type="text"
//         placeholder="Student ID"
//         value={studentId}
//         onChange={(e) => setStudentId(e.target.value)}
//       />

//       <input
//         className="border p-2 w-full"
//         type="text"
//         placeholder="Name"
//         value={name}
//         onChange={(e) => setName(e.target.value)}
//       />

//       <button
//         className={`bg-blue-500 text-white px-4 py-2 rounded ${loading ? "opacity-50" : ""}`}
//         onClick={handleCheckIn}
//         disabled={loading}
//       >
//         {loading ? "Processing..." : "Check-in"}
//       </button>

     

//       <h2 className="text-lg font-bold mt-4">Today's Attendance</h2>

//      <p className="text-gray-700 font-semibold">Total Students: {totalStudents}</p>

//       {attendance.length > 0 ? (
//         <ul className="border p-2 rounded">
//           {attendance.map((record, index) => (
//             <li key={index} className="border-b p-2">
//               <strong>{record.name}</strong> - {record.student_id} <br />
//               <span className="text-gray-500 text-sm">{record.date}</span>
//             </li>
//           ))}
//         </ul>
//       ) : (
//         <p className="text-gray-500">No attendance records yet.</p>
//       )}
//     </div>
//   );
// };

// export default App;



import React, { useState, useEffect } from "react";
import axios from "axios";
import FingerprintJS from "@fingerprintjs/fingerprintjs";

const App = () => {
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminId, setAdminId] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [studentId, setStudentId] = useState("");
  const [name, setName] = useState("");
  
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [deviceId, setDeviceId] = useState("");
  const [present_student, setpresentStudents] = useState(0);
  const [proxies_student, setproxiesStudents] = useState(0);

  useEffect(() => {
    const getFingerprint = async () => {
      const fp = await FingerprintJS.load();
      const result = await fp.get();
      setDeviceId(result.visitorId);
    };

    getFingerprint();
    fetchAttendance();
  }, []);

  const fetchAttendance = async () => {
    try {
      const response = await axios.get("http://localhost:5000/attendance");
      // console.log(response);
      setAttendance(response.data.students);
      setpresentStudents(response.data.total_present);
      setproxiesStudents(response.data.total_proxy);
      
    } catch (error) {
      console.error("Error fetching attendance:", error);
    }
  };

  const handleAdminLogin = async () => {
    try {
      const response = await axios.post("http://localhost:5000/admin_login", {
        admin_id: adminId,
        password: adminPassword,
      });
      alert(response.data.message);
      setIsAdmin(true);
    } catch (error) {
      alert("Invalid admin credentials");
    }
  };

  const submitAdminLocation = async () => {
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const latitude = pos.coords.latitude;
        const longitude = pos.coords.longitude;

        try {
          await axios.post("http://localhost:5000/admin_location", {
            latitude,
            longitude,
          });

          alert("Admin location updated!");
        } catch (error) {
          console.error("Error updating location:", error);
          alert("Error updating location.");
        }
      },
      (err) => {
        console.error("Error getting location:", err);
        alert("Location access is required.");
      }
    );
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
          const studentData = {
            student_id: studentId,
            name,
            latitude,
            longitude,
            device_id: deviceId,
          };

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
            await handleMarkAttendance(studentData);
          }

          setLoading(false);
         
          
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
    const handleMarkAttendance = async (checkinresponse) => {
    try {
      setLoading(true);
      const studentData = checkinresponse;  // ✅ Get the actual data

      console.log("Marking Attendance with Data:", studentData);
  
      const response = await axios.post("http://localhost:5000/mark_attendance", studentData);
      // const response=await axios.post("http://localhost:5000/mark_attendance",checkinresponse);

    
      if (response.data.warning) {
        alert(response.data.warning);
      } else {
        alert("Attendance marked successfully!");
        setLoading(false);
        fetchAttendance();
      }
    }
     catch (error) {
      setLoading(false);
      console.error("Error marking attendance:", error);
      alert("Error marking attendance. Please try again.");
    }
  };
  

  return (
    <div className="p-6 max-w-lg mx-auto bg-white rounded-xl shadow-md space-y-4">
      {!isAdmin ? (
        <>
          <h2 className="text-lg font-bold">Admin Login</h2>

          <input
            className="border p-2 w-full"
            type="text"
            placeholder="Admin ID"
            value={adminId}
            onChange={(e) => setAdminId(e.target.value)}
          />
          <input
            className="border p-2 w-full"
            type="password"
            placeholder="Password"
            value={adminPassword}
            onChange={(e) => setAdminPassword(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleAdminLogin}>
            Login
          </button>

          <h1 className="text-xl font-bold mt-6">Student Check-in</h1>
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
            className={`bg-green-500 text-white px-4 py-2 rounded ${loading ? "opacity-50" : ""}`}
            onClick={handleCheckIn}
            disabled={loading}
          >
            {loading ? "Processing..." : "Check-in"}
          </button>
        </>
      ) : (
        <>
          <h2 className="text-lg font-bold">Admin Dashboard</h2>

          <button className="bg-green-500 text-white px-4 py-2 rounded" onClick={submitAdminLocation}>
            Submit Current Location
          </button>
        

          <h3 className="text-lg font-bold mt-4">Today's Attendance</h3>
        

          {attendance.length > 0 ? (
  <div className="border p-2 rounded">
    {/* ✅ Regular Attendance */}
    <h3 className="text-green-600 font-bold mb-2">Present Students</h3>
    <p className="text-gray-700 font-semibold">Total Present: {present_student}</p>
    <ul>
      {attendance.filter(record => record.status !== 'Proxy').map((record, index) => (
        <li key={index} className="border-b p-2 text-green-500">
          <strong>{record.name}</strong> - {record.student_id} <br />
          <span className="text-gray-500 text-sm">{record.date} </span>
        </li>
      ))}
    </ul>

    {/* ❌ Proxy Attendance */}
    <h3 className="text-red-600 font-bold mt-4">Proxy Attempts</h3>
    <p className="text-gray-700 font-semibold">Total Proxies: {proxies_student}</p>
    <ul>
      {attendance.filter(record => record.status === 'Proxy').map((record, index) => (
        <li key={index} className="border-b p-2 text-red-500">
          <strong>{record.name}</strong> - {record.student_id} <br />
          <span className="text-gray-500 text-sm">{record.date}</span>
        </li>
      ))}
    </ul>
  </div>
) : (
  <p className="text-gray-500">No attendance records yet.</p>
)}

        </>
      )}
    </div>
  );
};

export default App;