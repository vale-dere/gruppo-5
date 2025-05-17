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
