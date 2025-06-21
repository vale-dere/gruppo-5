import React from 'react';
import '../styles/Login.css';
import WhiteBox from './WhiteBox';
import backgroundImage from '../assets/banner-bg.jpg';
import iconImage from '../assets/login_icon.png';
import { useNavigate } from 'react-router-dom';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { auth } from '../firebase';

const LoginPage = () => {
  const navigate = useNavigate();

  const handleGoogleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      const token = await result.user.getIdToken();
      localStorage.setItem('firebaseToken', token);
      navigate('/home');
    } catch (error) {
      console.error('Errore durante il login con Google:', error);
      alert('Autenticazione fallita. Riprova.');
    }
  };

  return (
    <div className="login-page">
      <div
        className="login-background"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      />
      <div className="login-content">
        <WhiteBox title="" className="login-box-large">
          <div className="login-form">
            <img src={iconImage} alt="Login Icon" className="login-icon" />
            <h2 className="login-title">
              Login to <span className="highlight">AnonimaData</span>
            </h2>
            <button onClick={handleGoogleLogin} className="button google-button">
              Accedi con Google
            </button>
          </div>
        </WhiteBox>
      </div>
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