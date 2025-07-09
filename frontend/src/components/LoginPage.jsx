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
      console.error("Error during Google login:", error);
      alert("Authentication failed. Please try again.");
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
              Login with Google
            </button>
          </div>
        </WhiteBox>
      </div>
    </div>
  );
};

export default LoginPage;


/*
What this component does:
1- When you click the button, it opens the Google popup.
2- After login, Firebase returns the authenticated user.
3- From the user, you get the Firebase ID Token (JWT).
4- You can save it in localStorage to send to the backend (e.g., as a Bearer Token).
5- Redirects to the protected page (e.g., /home).
*/