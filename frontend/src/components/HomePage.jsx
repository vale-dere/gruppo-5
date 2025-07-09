import React, { useState } from 'react';
import '../styles/App.css';
import backgroundImage from '../assets/banner-bg.jpg';
import '../styles/ButtonUpload.css'; 

import WhiteBox from './WhiteBox';
import FileUpload from './FileUpload';
import AlgorithmSelector from './AlgorithmSelector';
import { useNavigate } from 'react-router-dom';
import { getAuth, signOut, getIdToken } from "firebase/auth";

function HomePage() {  
  const navigate = useNavigate(); 
  const auth = getAuth();
 
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("");
  const [parameterValue, setParameterValue] = useState("");
  const [previewData, setPreviewData] = useState([]);   
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [downloadFileId, setDownloadFileId] = useState(null); 
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadMessage, setDownloadMessage] = useState("");

  const handleLogout = () => {
    signOut(auth)
      .then(() => {
        // successfully logged out
        navigate('/'); // Redirect to login page
      })
      .catch((error) => {
        console.error("Error during logout:", error);
      });
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleAlgorithmChange = (e) => {
    setSelectedAlgorithm(e.target.value);
    setParameterValue("");  // reset parameter when changing algorithm
  };

  const handleParameterChange = (e) => {
    setParameterValue(e.target.value);
  };

  const handleAnonymize = async () => {
    console.log("Sending anonymization request", selectedFile, selectedAlgorithm, parameterValue); //debug purposes

    // reset download link
    if (downloadUrl) {
      URL.revokeObjectURL(downloadUrl);
      setDownloadUrl(null);
    }

    if (!selectedFile || !selectedAlgorithm || !parameterValue.trim()) {
      alert("Please fill in all fields and make sure the parameter is valid");
      return;
    }

    const cleanParameter = String(parameterValue).replace(',', '.');
    if (isNaN(Number(cleanParameter))) {
      alert("The parameter must be a valid number (e.g. 0.1 or 3)");
      return;
    }
  
    const form = new FormData();
    form.append("file", selectedFile);
    form.append("algorithm", selectedAlgorithm);  // es. "k-anonymity"
    form.append("parameter", cleanParameter);     // es. "2" o "0.5"

    //********* authentication */
    try {
      const user = auth.currentUser;
      if (!user) {
        alert("User not authenticated.");
        return;
      }
    
      const token = await getIdToken(user, true); // true for force refresh
    //*********** */

      const BASE_URL = import.meta.env.VITE_API_BASE_URL; 
      console.log("Base URL:", BASE_URL); // debug purposes
      const res = await fetch(`${BASE_URL}/anonymize`, {
        method: "POST",
        body: form,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      console.log("Status:", res.status);

      const text = await res.text(); // don't use .json() immediately
     
      if (!res.ok) {
        if (res.status === 401) {
          alert("Session expired. Please log in again.");
          await signOut(auth);     // automatic logout
          navigate("/");           // redirect
          return;
      }
      const error = JSON.parse(text);
      alert("Backend error: " + error.detail);
      return;
    }
    const json = JSON.parse(text);
    setPreviewData(json.preview || []);
    setDownloadUrl(json.download_url);
    setDownloadFileId(json.download_file_id); // <--- save file_id
    } catch (err) {
      console.error("Network error:", err);
      alert("Error during anonymization. Network error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Function to download the anonymized file with Bearer token authentication
  const handleDownloadFull = async () => {
    if (!downloadUrl) {
      alert("No file to download. Please anonymize the dataset first.");
      return;
    }

    if (!downloadFileId) {
      alert("No file to download. Please anonymize the dataset first.");
    return;
    }
    
    setIsDownloading(true);
    setDownloadMessage("Downloading...");

    try {
      const user = auth.currentUser;
      if (!user) {
        alert("User not authenticated.");
        setIsDownloading(false);
        setDownloadMessage("");
        return;
      }
      const token = await getIdToken(user, true);

      const BASE_URL = import.meta.env.VITE_API_BASE_URL; 
      const res = await fetch(`${BASE_URL}/download/${downloadFileId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.status === 401) {
      alert("Session expired. Please log in again.");
      await signOut(auth);
      navigate("/");
      return;
      }

      if (!res.ok) {
        const errorText = await res.text();
        alert("Error during download: " + errorText);
        setIsDownloading(false);
        setDownloadMessage("");
        return;
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;

      const filename = downloadUrl.split("/").pop() || "anonymized_dataset_full.csv";
      a.download = filename;

      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setDownloadMessage("Download complete!");
    } catch (err) {
      console.error("File download error:", err);
      alert("Error during download: " + err.message);
      setDownloadMessage("");
    } finally {
      setIsDownloading(false);
      setTimeout(() => setDownloadMessage(""), 3000); // clear message after 3 sec
    }
  };

  return (
    <div className="App">
      <section className="title-section">
        {/* White banner with logout */}
      <header className="header-overlay">
        <button 
          type="button"
          className="button" 
          onClick={handleLogout}
        >
          Logout
        </button> 
      </header>
        <div className="title-content">
          <h1>AnonimaData</h1>
          <p>Upload and anonymize your datasets</p>
        </div>
      </section>

      {/* Main content */}
      <section className="body-section">
        <WhiteBox title="Upload your dataset">
          <FileUpload selectedFile={selectedFile} onFileChange={handleFileChange} />
        </WhiteBox>

        <WhiteBox title="Choose anonymization algorithm">
          <AlgorithmSelector
            selectedAlgorithm={selectedAlgorithm}
            onAlgorithmChange={handleAlgorithmChange}
            parameterValue={parameterValue}
            onParameterChange={handleParameterChange}
          />

        </WhiteBox>

        {/* Button to Anonymize */}
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button
            type="button"
            className="anonymize-button"
            disabled={!selectedFile || !selectedAlgorithm || !parameterValue || !parameterValue.trim()}
            onClick={handleAnonymize}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
            Anonymize
          </button>
        </div>

        {/* Preview of anonymized data */}
        <WhiteBox title="Preview Anonymized Data" >
          {previewData.length > 0 ? (
            <div style={{ overflowX: 'auto', backgroundColor: 'white', padding: '10px', borderRadius: '6px'}}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr>
                    {Object.keys(previewData[0]).map(col => (
                      <th key={col} style={{ border: '1px solid #ccc', padding: '8px', backgroundColor: '#f5f5f5' }}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {previewData.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((val, i) => (
                        <td key={i} style={{ border: '1px solid #eee', padding: '8px' }}>{val}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p style={{ textAlign: 'center', marginTop: '20px' }}>
              Upload and anonymize a file to see the preview.
            </p>
          )}
  

        {previewData.length > 0 && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <button
            type="button"
            className="anonymize-button"
            onClick={handleDownloadFull}
            disabled={isDownloading}
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
              <path d="M12 5v14M5 12l7 7 7-7" />
            </svg>
            Download full anonymized file
            {isDownloading && <span className="spinner" style={{ marginLeft: 10 }}></span>}
          </button>

          {downloadMessage && (
            <div style={{ marginTop: '10px', color: isDownloading ? 'blue' : 'green' }}>
              {downloadMessage}
            </div>
          )}
        </div>
      )}

        </WhiteBox>
      <div style={{ paddingBottom: '40px' }}></div>
      </section>
    </div>
);
}

export default HomePage;


