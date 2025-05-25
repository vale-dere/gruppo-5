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
  //Aggiuno uno stato per la preview del dataset
  const [parameterValue, setParameterValue] = useState("");
  const [previewData, setPreviewData] = useState([]);   
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleAlgorithmChange = (e) => {
    setSelectedAlgorithm(e.target.value);
    setParameterValue("");  // reset parametro quando cambio algoritmo
  };

  const handleParameterChange = (e) => {
    setParameterValue(e.target.value);
  };

  /* commento momentaneo. capire se meglio questo o codice nuovo (vedi subito dopo)
  // Funzione per chiamare il backend
  const handleAnonymize = async () => {
    if (!selectedFile || !selectedAlgorithm) return;
    setLoading(true);
    const form = new FormData();
    form.append('file', selectedFile);
// passa il parametro dinamico (nome “k” o “epsilon” a seconda dell’algoritmo)
    const paramName = selectedAlgorithm === 'differential-privacy' ? 'epsilon' : 'k';
    form.append(paramName, parameterValue); 
    try {
      const res = await fetch('http://localhost:8080/anonymize', {
        method: 'POST',
        body: form
      });
      const json = await res.json();
      setPreviewData(json.preview || []);
    } catch (err) {
      console.error(err);
      alert('Errore durante l’anonymization');
    } finally {
      setLoading(false);
    }
  };
  */
  const handleAnonymize = async () => {
    console.log("Sending anonymization request", selectedFile, selectedAlgorithm, parameterValue); //debug purposes

    if (!selectedFile || !selectedAlgorithm || !parameterValue) return;
    setLoading(true);
  
    const form = new FormData();
    form.append("file", selectedFile);
    form.append("algorithm", selectedAlgorithm);  // es. "k-anonymity"
    form.append("parameter", parameterValue);     // es. "2" o "0.5"
  
    try {
      const res = await fetch("http://localhost:8080/anonymize", {
        method: "POST",
        body: form,
      });
  
      console.log("Status:", res.status);

      const text = await res.text(); // non usare .json() subito
      console.log("Raw response:", text);

      if (!res.ok) { //debug purposes
      const error = JSON.parse(text);
      alert("Errore backend: " + error.detail);
      return;
  }

      const json = JSON.parse(text); // parsing manuale
      setPreviewData(json.preview || []);
    } catch (err) {
      console.error("Errore di rete:", err);
      alert("Errore durante l’anonimizzazione. Errore di rete: " + err.message);
    } finally {
      setLoading(false);
    }
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
            parameterValue={parameterValue}
            onParameterChange={handleParameterChange}
          />

        </WhiteBox>

        {/* Bottone Anonymize */}
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button
            type="button"
            className="anonymize-button"
            disabled={!selectedFile || !selectedAlgorithm || !parameterValue}
            onClick={handleAnonymize}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
            Anonymize
          </button>
        </div>
      
        {/* Preview dei dati anonimizzati */}
        <WhiteBox title="Preview Anonymized Data">
  {previewData.length > 0 ? (
    <div style={{ overflowX: 'auto', backgroundColor: 'white', padding: '10px', borderRadius: '6px' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {Object.keys(previewData[0]).map(col => (
              <th key={col} style={{ border: '1px solid #ccc', padding: '8px', backgroundColor: '#f5f5f5' }}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {previewData.map((row, idx) => (
            <tr key={idx}>
              {Object.values(row).map((val, i) => (
                <td key={i} style={{ border: '1px solid #eee', padding: '8px' }}>{val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ) : (
    <p style={{ textAlign: 'center', marginTop: '20px' }}>
      Upload and anonymize a file to see the preview.
    </p>
  )}
</WhiteBox>
 
      </section>
    </div>
);
}

export default HomePage;
