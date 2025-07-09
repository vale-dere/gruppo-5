// Guard that checks if the user is logged in before showing the homepage; otherwise, redirects to login

import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { getAuth, onAuthStateChanged } from "firebase/auth";

const PrivateRoute = ({ children }) => {
  const [loading, setLoading] = useState(true);   // Loading state
  const [user, setUser] = useState(null);
  const auth = getAuth();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);  // Finished loading
    });

    return () => unsubscribe();  // Cleanup listener
  }, [auth]);

  if (loading) {
    return <div>Loading...</div>;  // Or a spinner
  }

  if (!user) {
    return <Navigate to="/" replace />;  // If not logged in, redirect to login
  }

  return children;  // If logged in, show the protected page
};

export default PrivateRoute;
