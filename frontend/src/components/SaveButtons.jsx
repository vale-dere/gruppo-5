export default function SaveButtons({ dataset }) {
  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(dataset, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'anonymized_dataset.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleSaveToDatabase = async () => {
    try {
      await fetch('http://localhost:8000/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: dataset })
      });
      alert('Dataset salvato con successo!');
    } catch (err) {
      alert('Errore durante il salvataggio nel database.');
    }
  };

  if (!dataset || dataset.length === 0) return null;

  return (
    <div className="flex gap-4">
      <button onClick={handleSaveToDatabase} className="px-4 py-2 bg-green-600 text-white rounded">
        Salva nel Database
      </button>
      <button onClick={handleDownload} className="px-4 py-2 bg-blue-500 text-white rounded">
        Scarica CSV
      </button>
    </div>
  );
}