//guardia che controlla se l'utenet è loggato prima di mostrare homepage, in caso contrario reindirizza a login

import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { getAuth, onAuthStateChanged } from "firebase/auth";

const PrivateRoute = ({ children }) => {
  const [loading, setLoading] = useState(true);   // Caricamento in corso
  const [user, setUser] = useState(null);
  const auth = getAuth();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);  // Finito di caricare
    });

    return () => unsubscribe();  // Pulizia listener
  }, [auth]);

  if (loading) {
    return <div>Loading...</div>;  // Oppure uno spinner
  }

  if (!user) {
    return <Navigate to="/" replace />;  // Se non loggato, redirect a login
  }

  return children;  // Se loggato, mostra la pagina protetta
};

export default PrivateRoute;
