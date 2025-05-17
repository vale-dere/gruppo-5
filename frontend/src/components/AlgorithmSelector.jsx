import React from 'react';

export default function AlgorithmSelector({ selectedAlgorithm, onAlgorithmChange }) {
  return (
    <>
      <select
        className={`algorithm-select ${selectedAlgorithm ? "selected" : ""}`}
        value={selectedAlgorithm}
        onChange={onAlgorithmChange}
        style={{
          color: selectedAlgorithm ? '#000000' : '#999999',
        }}
      >
        <option value="">Select an algorithm</option>
        <option value="k-anonymity">k-Anonymity</option>
        <option value="l-diversity">l-Diversity</option>
        <option value="t-closeness">t-Closeness</option>
        <option value="differential-privacy">Differential Privacy</option>
      </select>

      {selectedAlgorithm === "k-anonymity" && (
        <div className="parameter-section">
            <label htmlFor="k">k (anonymity level):</label>
            <input
            id="k"
            type="number"
            min="1"
            placeholder="e.g. 3"
            className="parameter-input"
            />
        </div>
        )}

        {selectedAlgorithm === "differential-privacy" && (
        <div className="parameter-section">
            <label htmlFor="epsilon">Epsilon (privacy budget):</label>
            <input
            id="epsilon"
            type="number"
            min="0"
            step="0.01"
            placeholder="e.g. 0.5"
            className="parameter-input"
            />
        </div>
        )}
    </>
  );
}
