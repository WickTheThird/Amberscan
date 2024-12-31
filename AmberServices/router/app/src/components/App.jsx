import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

// Components
import Authentication from "./Authentication";
import DropFiles from "./DropFiles";
import MainScreen from "./MainScreen";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authHash, setAuthHash] = useState(null);

  const handleAuthentication = (hash) => {
    setIsAuthenticated(true);
    setAuthHash(hash);
  };

  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route
          path="/login"
          element={
            <Authentication isSignUp={false} onAuth={handleAuthentication} />
          }
        />
        <Route
          path="/signup"
          element={
            <Authentication isSignUp={true} onAuth={handleAuthentication} />
          }
        />

        {/* Protected Routes */}
        <Route
          path="/home"
          element={
            isAuthenticated ? (
              <MainScreen authHash={authHash} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route
          path="/drop-files"
          element={
            isAuthenticated ? (
              <DropFiles authHash={authHash} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        {/* Catch-All Route */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
