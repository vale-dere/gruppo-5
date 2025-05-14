import FileUpload from '../components/FileUpload';
import AlgorithmSelector from '../components/AlgorithmSelector';
import AlgorithmConfigForm from '../components/AlgorithmConfigForm';
import PreviewTable from '../components/PreviewTable';
import SaveButtons from '../components/SaveButtons';
import { useState } from 'react';

export default function DashboardPage() {
  const [dataset, setDataset] = useState(null);
  const [algorithm, setAlgorithm] = useState('');
  const [config, setConfig] = useState({});
  const [preview, setPreview] = useState([]);

  const handleAnonymize = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/anonymize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset,
        algorithm,
        config
      })
    });
    const anonymized = await res.json();
    setPreview(anonymized);
  } catch (err) {
    alert('Errore durante l\'anonimizzazione');
  }
};

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h2 className="text-xl font-semibold mb-4">Dashboard</h2>
      <FileUpload onLoad={setDataset} />
      <AlgorithmSelector onSelect={setAlgorithm} />
      <AlgorithmConfigForm algorithm={algorithm} onChange={setConfig} />
      <button
  onClick={handleAnonymize}
  className="mb-4 px-4 py-2 bg-purple-600 text-white rounded"
>
  Avvia Anonimizzazione
</button>
      <PreviewTable data={preview} />
      <SaveButtons dataset={preview} />
    </div>
  );

  
}