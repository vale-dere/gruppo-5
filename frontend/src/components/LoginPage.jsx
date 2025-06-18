/*
import React, { useState } from 'react';
import '../styles/Login.css';
import WhiteBox from './WhiteBox';
import backgroundImage from '../assets/banner-bg.jpg';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    console.log('Email:', email, 'Password:', password);
    navigate('/home'); // Simula login
  };

  return (
    <div className="login-page">
      <div
        className="login-background"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      />
      <div className="login-content">
      <WhiteBox title="Login to AnonimaData" className="login-box">
        <form className="login-form" onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            className="login-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            className="login-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className="button">Login</button>
        </form>
      </WhiteBox>
      </div>
    </div>
  );
}
*/

import React from 'react';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { auth } from '../firebase'; // Assicurati che firebase.js sia importato correttamente
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const navigate = useNavigate();

  const handleGoogleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);

      // Recupera l'ID token (JWT) da inviare al backend
      const token = await result.user.getIdToken();

      // Salva il token localmente (es. per fetch protette)
      localStorage.setItem('firebaseToken', token);

      // 🔁 Redirect alla pagina protetta
      navigate('/home');
    } catch (error) {
      console.error('Errore durante il login con Google:', error);
      alert('Autenticazione fallita. Riprova.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Login</h2>
      <button onClick={handleGoogleLogin}>
        Accedi con Google
      </button>
    </div>
  );
};

export default LoginPage;

/*
Cosa fa questo componente:
1- Quando clicchi sul pulsante, apre il popup di Google.
2- Dopo il login, Firebase restituisce l’utente autenticato.
3- Dal user, ottieni il Firebase ID Token (JWT).
4- Puoi salvarlo in localStorage per inviarlo al backend (es. come Bearer Token).
5- Redirect alla pagina protetta (es. /home).
*/