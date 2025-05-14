import React from 'react';

function AlgorithmSelector() {
  return (
    <div style={{ marginBottom: '2rem' }}>
      <label>
        Seleziona algoritmo:
        <select defaultValue="k-anonymity" disabled>
          <option value="k-anonymity">k-Anonymity</option>
        </select>
      </label>
    </div>
  );
}

export default AlgorithmSelector;
