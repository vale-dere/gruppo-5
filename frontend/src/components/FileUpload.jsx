import React from 'react';
import '../styles/ButtonUpload.css'; // Riutilizza gli stili già usati

export default function FileUpload({ selectedFile, onFileChange }) {
  return (
    <div className="file-input-wrapper">
      {/* Box a sinistra con nome file */}
      <div className="file-name-box">
        {selectedFile ? selectedFile.name : "No file selected"}
      </div>
    
    {/* per ora commento perchè non mi va il bottone
      {/* Bottone upload */}{/*
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
      */}

      <label className="anonymize-button" style={{ cursor: 'pointer' }} >
      <input
        type="file"
        accept=".csv, .json"
        onChange={onFileChange}
        style={{ display: 'none' }}
      />
        <svg 
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              viewBox="0 0 24 24" 
              width="20"
              height="20" >
              <path d="M4 4v16h16V4H4zm8 12v-4M8 12l4-4 4 4" />
              </svg>
        {selectedFile ? "Change File" : "Upload Dataset"}
    </label>
  </div>
  );
}
