import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

// Components
import Authentication from "./Authentication";
import MainScreen from "./MainScreen";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authData, setAuthData] = useState({
    signature: null,
    clientName: null,
  });

  // Load authentication state from localStorage on app load
  useEffect(() => {
    const storedSignature = localStorage.getItem("auth_signature");
    const storedClientName = localStorage.getItem("client_name");

    if (storedSignature && storedClientName) {
      setIsAuthenticated(true);
      setAuthData({
        signature: storedSignature,
        clientName: storedClientName,
      });
    }
  }, []);

  // Handle authentication and persist signature and client name
  const handleAuthentication = (signature, clientName) => {
    setIsAuthenticated(true);
    setAuthData({ signature, clientName });
    localStorage.setItem("auth_signature", signature);
    localStorage.setItem("client_name", clientName);
  };

  // Handle logout
  const handleLogout = () => {
    setIsAuthenticated(false);
    setAuthData({ signature: null, clientName: null });
    localStorage.removeItem("auth_signature");
    localStorage.removeItem("client_name");
  };

  return (
    <Router>
      <Routes>
        {/* Default Route */}
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Navigate to="/home" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        {/* Login Route */}
        <Route
          path="/login"
          element={
            isAuthenticated ? (
              <Navigate to="/home" replace />
            ) : (
              <Authentication isSignUp={false} onAuth={handleAuthentication} />
            )
          }
        />
        {/* Signup Route */}
        <Route
          path="/signup"
          element={
            isAuthenticated ? (
              <Navigate to="/home" replace />
            ) : (
              <Authentication isSignUp={true} onAuth={handleAuthentication} />
            )
          }
        />
        {/* Home Route */}
        <Route
          path="/home"
          element={
            isAuthenticated ? (
              <MainScreen authData={authData} onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        {/* Catch-All Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
