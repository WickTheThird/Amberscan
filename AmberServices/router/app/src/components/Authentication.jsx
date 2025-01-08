import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Authentication({ isSignUp, onAuth }) {
  const api = "http://127.0.0.1:8000/";
  const navigate = useNavigate();

  const [signUp, setIsSignUp] = useState(isSignUp);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSignUp = async () => {
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match!");
      return;
    }

    try {
      const response = await fetch(api + "register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Signup failed!");
      }

      alert("Sign-up successful. Please log in.");
      setIsSignUp(false);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleLogIn = async () => {
    setError("");

    try {
      const response = await fetch(api + "login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Login failed!");
      }

      const data = await response.json();
    //   console.log("Login successful:", data);

      if (onAuth) {
        onAuth(data.signature, formData.username);
      }

      navigate("/home");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      {signUp ? (
        <SignUp
          formData={formData}
          handleInputChange={handleInputChange}
          handleSignUp={handleSignUp}
          setIsSignUp={setIsSignUp}
          error={error}
        />
      ) : (
        <LogIn
          formData={formData}
          handleInputChange={handleInputChange}
          handleLogIn={handleLogIn}
          setIsSignUp={setIsSignUp}
          error={error}
        />
      )}
    </div>
  );
}

const SignUp = ({
  formData,
  handleInputChange,
  handleSignUp,
  setIsSignUp,
  error,
}) => (
  <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div className="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-center text-gray-700 mb-4">
        Sign Up
      </h2>
      {error && <p className="text-red-500 text-center">{error}</p>}
      <div className="space-y-4">
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleInputChange}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleInputChange}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleInputChange}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={handleSignUp}
          className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-600"
        >
          Sign Up
        </button>
      </div>
      <button
        onClick={() => setIsSignUp(false)}
        className="w-full mt-4 text-sm text-blue-500 hover:underline"
      >
        Already have an account?
      </button>
    </div>
  </div>
);

const LogIn = ({
  formData,
  handleInputChange,
  handleLogIn,
  setIsSignUp,
  error,
}) => (
  <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div className="w-full max-w-md bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-center text-gray-700 mb-4">
        Log In
      </h2>
      {error && <p className="text-red-500 text-center">{error}</p>}
      <div className="space-y-4">
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleInputChange}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={handleLogIn}
          className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-600"
        >
          Log In
        </button>
      </div>
      <button
        onClick={() => setIsSignUp(true)}
        className="w-full mt-4 text-sm text-blue-500 hover:underline"
      >
        Don't have an account?
      </button>
    </div>
  </div>
);

export default Authentication;
