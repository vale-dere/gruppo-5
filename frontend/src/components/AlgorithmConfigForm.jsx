export default function AlgorithmConfigForm({ algorithm, onChange }) {
  const handleInput = (e) => {
    onChange(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  if (!algorithm) return null;

  const configFields = {
    'k-anonymity': [{ name: 'k', label: 'k (>=2)', type: 'number' }],
    'l-diversity': [{ name: 'l', label: 'l (>=2)', type: 'number' }],
    't-closeness': [{ name: 't', label: 't (0-1)', type: 'number', step: '0.01' }],
    'differential-privacy': [{ name: 'epsilon', label: 'ε (privacy loss)', type: 'number', step: '0.01' }]
  };

  return (
    <div className="mb-4">
      <label className="block mb-1 font-medium">Configure Parameters</label>
      {configFields[algorithm].map(field => (
        <div key={field.name} className="mb-2">
          <label className="block text-sm">{field.label}</label>
          <input {...field} className="w-full p-2 border rounded" onChange={handleInput} />
        </div>
      ))}
    </div>
  );
}