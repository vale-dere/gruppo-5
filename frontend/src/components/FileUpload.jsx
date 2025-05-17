import React from 'react';

export default function FileUpload({ selectedFile, onFileChange }) {
  return (
    <div className="file-input-wrapper">
      {/* Box a sinistra con nome file */}
      <div className="file-name-box">
        {selectedFile ? selectedFile.name : "No file selected"}
      </div>

      {/* Bottone upload */}
      <input
        id="fileUpload"
        type="file"
        accept=".csv, .json"
        onChange={onFileChange}
        style={{ display: 'none' }}
      />

      <label htmlFor="fileUpload">
        <button type="button">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            viewBox="0 0 24 24"
          >
            <path d="M4 4v16h16V4H4zm8 12v-4M8 12l4-4 4 4" />
          </svg>
          Upload dataset
        </button>
      </label>
    </div>
  );
}
