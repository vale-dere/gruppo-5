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
      const res = await fetch('http://localhost:8000/anonymize', {
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
            disabled={!selectedFile || !selectedAlgorithm}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
            Anonymize
          </button>
        </div>
      
        {/* Preview dei dati anonimizzati */}
        {previewData.length > 0 && (
          <div className="preview-table" style={{ maxWidth: '800px', margin: '40px auto' }}>
            <h3>Preview Anonymized Data</h3>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  {Object.keys(previewData[0]).map(col => (
                    <th key={col} style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>
                    {col}
                   </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {previewData.map((row, idx) => (
                  <tr key={idx}>
                    {Object.values(row).map((val, i) => (
                      <td key={i} style={{ border: '1px solid #eee', padding: '8px' }}>
                        {val}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

export default HomePage;
