export default function AlgorithmSelector({ onSelect }) {
  return (
    <div className="mb-4">
      <label className="block mb-1 font-medium">Choose Algorithm</label>
      <select className="w-full p-2 border rounded" onChange={e => onSelect(e.target.value)}>
        <option value="">-- Select --</option>
        <option value="k-anonymity">k-Anonymity</option>
        <option value="l-diversity">l-Diversity</option>
        <option value="t-closeness">t-Closeness</option>
        <option value="differential-privacy">Differential Privacy</option>
      </select>
    </div>
  );
}