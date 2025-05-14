export default function PreviewTable({ data }) {
  if (!data || data.length === 0) return null;

  const headers = Object.keys(data[0]);
  const previewData = data.slice(0, 10);

  return (
    <div className="mb-4 overflow-x-auto">
      <h3 className="font-medium mb-2">Preview (first 10 rows)</h3>
      <table className="table-auto border w-full text-sm">
        <thead>
          <tr>
            {headers.map(h => <th key={h} className="border px-2 py-1 bg-gray-100">{h}</th>)}
          </tr>
        </thead>
        <tbody>
          {previewData.map((row, i) => (
            <tr key={i}>
              {headers.map(h => <td key={h} className="border px-2 py-1">{row[h]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
