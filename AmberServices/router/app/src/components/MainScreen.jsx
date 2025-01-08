import React, { useState, useEffect } from "react";
import {
  FaSearch,
  FaUpload,
  FaSignOutAlt,
  FaFileAlt,
  FaUserShield,
  FaHome,
} from "react-icons/fa";

function MainScreen({ authHash, onLogout }) {
  const api = "http://127.0.0.1:8000/";
  const [isAdmin, setIsAdmin] = useState(false);
  const [files, setFiles] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [uploadFile, setUploadFile] = useState(null);
  const [fileType, setFileType] = useState("image");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (authHash === undefined) {
    authHash = [
      localStorage.getItem("auth_signature"),
      localStorage.getItem("client_name"),
    ];
  }

  // Check user permissions
  useEffect(() => {
    fetch(api + "permissions/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authHash[0]}`,
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => setIsAdmin(data.is_admin))
      .catch(() => setError("Failed to verify permissions"));
  }, [authHash[0]]);

  // Handle search
  const handleSearch = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        api + (isAdmin ? "admin_files/" : "user_files/"),
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authHash[0]}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) throw new Error("Failed to fetch files");

      const data = await response.json();
      setFiles(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!uploadFile) {
      setError("Please select a file to upload");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append(fileType, uploadFile);
    formData.append("provider", authHash[0]);
    formData.append("client", authHash[1]);
    formData.append("name", uploadFile.name);

    try {
      const response = await fetch(
        api + `${authHash[0]}/upload_${fileType}/`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${authHash[0]}`,
          },
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to upload file");
      }

      alert("File uploaded successfully!");
      setUploadFile(null);
      handleSearch();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <nav className="bg-blue-600 text-white w-64 flex flex-col">
        <div className="py-4 px-6 text-2xl font-bold flex items-center space-x-2">
          <FaHome />
          <span>Dashboard</span>
        </div>
        <ul className="flex-grow space-y-4 mt-8">
          <li>
            <button
              onClick={handleSearch}
              className="flex items-center space-x-2 w-full px-6 py-3 text-left hover:bg-blue-700 transition duration-200"
            >
              <FaSearch />
              <span>Search Files</span>
            </button>
          </li>
          <li>
            <button
              onClick={() => {}}
              className="flex items-center space-x-2 w-full px-6 py-3 text-left hover:bg-blue-700 transition duration-200"
            >
              <FaUpload />
              <span>Upload Files</span>
            </button>
          </li>
          {isAdmin && (
            <li>
              <button className="flex items-center space-x-2 w-full px-6 py-3 text-left hover:bg-blue-700 transition duration-200">
                <FaUserShield />
                <span>Admin Tools</span>
              </button>
            </li>
          )}
        </ul>
        <button
          onClick={onLogout}
          className="flex items-center space-x-2 w-full px-6 py-3 text-left hover:bg-red-700 transition duration-200"
        >
          <FaSignOutAlt />
          <span>Logout</span>
        </button>
      </nav>

      {/* Main Content */}
      <div className="flex-grow p-8">
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4 flex items-center space-x-2">
            <FaSearch />
            <span>Search Files</span>
          </h2>
          <div className="flex space-x-4">
            <input
              type="text"
              placeholder="Search term"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button
              onClick={handleSearch}
              className="flex items-center space-x-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition duration-200"
            >
              <FaSearch />
              <span>Search</span>
            </button>
          </div>
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4 flex items-center space-x-2">
            <FaUpload />
            <span>Upload Files</span>
          </h2>
          <div className="flex space-x-4 items-center">
            <select
              value={fileType}
              onChange={(e) => setFileType(e.target.value)}
              className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option value="image">Image</option>
              <option value="pdf">PDF</option>
            </select>
            <input
              type="file"
              onChange={(e) => setUploadFile(e.target.files[0])}
              className="px-4 py-2 border rounded-lg"
            />
            <button
              onClick={handleUpload}
              className="flex items-center space-x-2 bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition duration-200"
            >
              <FaUpload />
              <span>Upload</span>
            </button>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-semibold mb-4 flex items-center space-x-2">
            <FaFileAlt />
            <span>Files</span>
          </h2>
          {error && <p className="text-red-500 mb-4">{error}</p>}
          {loading ? (
            <p className="text-gray-700">Loading files...</p>
          ) : files.length > 0 ? (
            <ul className="space-y-2">
              {files.map((file) => (
                <li
                  key={file.id}
                  className="p-4 border rounded-lg shadow-sm hover:shadow-md transition duration-200"
                >
                  <p>
                    <strong>Name:</strong> {file.name}
                  </p>
                  <p>
                    <strong>Type:</strong> {file.type}
                  </p>
                  <p>
                    <strong>Uploaded By:</strong> {file.uploaded_by}
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-700">No files found</p>
          )}
        </div>
      </div>
    </div>
  );
}



export default MainScreen;
