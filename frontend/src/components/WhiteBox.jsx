import React from 'react';
import '../styles/App.css';  // Improve CSS here

export default function WhiteBox({ title, children }) {
  return (
    <div className="white-box">
      <h2>{title}</h2>
      <div className="white-box-content">
        {children}
      </div>
    </div>
  );
}