import React, { useState } from 'react';
import './styles.css';  // Importa il CSS
import UploadForm from './components/UploadForm';
import AlgorithmSelector from './components/AlgorithmSelector';

function App() {
  const [response, setResponse] = useState(null);

  return (
    <div className="container">
      <h1>Anonimizzazione Dati - Protezione Privacy</h1>
      <AlgorithmSelector />
      <UploadForm onResult={setResponse} />
      {response && (
        <div style={{ marginTop: '1rem' }}>
          <h3>Risultato:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
