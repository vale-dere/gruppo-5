import { useState } from 'react';
import Papa from 'papaparse';

export default function FileUpload({ onLoad }) {
  const [filename, setFilename] = useState('');

  const handleFile = e => {
    const file = e.target.files[0];
    if (!file) return;
    setFilename(file.name);

    const ext = file.name.split('.').pop();
    const reader = new FileReader();

    reader.onload = e => {
      if (ext === 'csv') {
        const result = Papa.parse(e.target.result, { header: true });
        onLoad(result.data);
      } else if (ext === 'json') {
        onLoad(JSON.parse(e.target.result));
      }
    };

    reader.readAsText(file);
  };

  return (
    <div className="mb-4">
      <label className="block mb-1 font-medium">Upload CSV or JSON</label>
      <input type="file" accept=".csv,.json" onChange={handleFile} />
      {filename && <p className="mt-2 text-sm text-gray-600">File: {filename}</p>}
    </div>
  );
}