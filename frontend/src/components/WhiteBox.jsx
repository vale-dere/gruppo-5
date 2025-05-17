import React from 'react';
import '../styles/App.css';  // Usa gli stili globali, o importa un css specifico se preferisci

export default function WhiteBox({ title, children }) {
  return (
    <div className='white-box'>
      <h2>{title}</h2>
      {children}
    </div>
  );
}
