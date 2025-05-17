import React, { useState } from 'react';
import '../styles/App.css';
import backgroundImage from '../assets/banner-bg.jpg';
import '../styles/ButtonUpload.css'; // Stili personalizzati per il bottone

import WhiteBox from './WhiteBox';
import FileUpload from './FileUpload';
import AlgorithmSelector from './AlgorithmSelector';
import { useNavigate } from 'react-router-dom';

function HomePage() {
  console.log("HomePage rendered");
  
  const navigate = useNavigate();  
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleAlgorithmChange = (e) => {
    setSelectedAlgorithm(e.target.value);
  };


  return (
    <div className="App">
      {/* Sezione con sfondo immagine */}
      <section className="title-section">
        {/* Banner bianco con logout*/}
      <header className="header-overlay">
        <button 
          type="button"
          className="button" 
          onClick={() => navigate('/')}
        >
          Logout
        </button> 
      </header>
      
        <div
          className="background-overlay"
          style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
        <div className="title-content">
          <h1>AnonimaData</h1>
          <p>Upload and anonymize your datasets</p>
        </div>
      </section>

      {/* Contenuto principale */}
      <section className="body-section">
        <WhiteBox title="Upload your dataset">
          <FileUpload selectedFile={selectedFile} onFileChange={handleFileChange} />
        </WhiteBox>

        <WhiteBox title="Choose anonymization algorithm">
          <AlgorithmSelector
            selectedAlgorithm={selectedAlgorithm}
            onAlgorithmChange={handleAlgorithmChange}
          />
        </WhiteBox>

        {/* Bottone Anonymize */}
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button
            type="button"
            className="anonymize-button"
            disabled={!selectedFile || !selectedAlgorithm}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
            Anonymize
          </button>
        </div>

      </section>
    </div>
  );
}

export default HomePage;
