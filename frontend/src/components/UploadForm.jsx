import React, { useState } from 'react';
import axios from 'axios';

function UploadForm({ onResult }) {
  const [file, setFile] = useState(null);
  const [k, setK] = useState(2);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`http://localhost:8080/upload?k=${k}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onResult(res.data);
    } catch (err) {
      console.error(err);
      onResult({ error: 'Errore durante l\'upload' });
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Seleziona il file (CSV):
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
      </label>
      <label>
        Valore di k:
        <input type="number" value={k} onChange={(e) => setK(e.target.value)} min="1" />
      </label>
      <button type="submit">Avvia Anonimizzazione</button>
    </form>
  );
}

export default UploadForm;
