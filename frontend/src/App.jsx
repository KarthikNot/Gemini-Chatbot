import { Routes, Route, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Chat from "./pages/Chat";
import { healthCheck } from "./api";

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const userId = localStorage.getItem('user_id');
  return userId ? children : <Navigate to="/login" replace />;
};

// Loading Component
const LoadingSpinner = () => (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div className="text-center">
      <div className="spinner mx-auto mb-4"></div>
      <p className="text-gray-600">Loading...</p>
    </div>
  </div>
);

export default function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [isServerOnline, setIsServerOnline] = useState(false);

  useEffect(() => {
    const checkServerHealth = async () => {
      try {
        await healthCheck();
        setIsServerOnline(true);
      } catch (error) {
        console.error('Server is not available:', error);
        setIsServerOnline(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkServerHealth();
  }, []);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isServerOnline) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-pink-100">
        <div className="text-center p-8 bg-white rounded-lg shadow-lg">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Server Unavailable</h1>
          <p className="text-gray-600 mb-4">
            The backend server is not running. Please start the server and refresh the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
