import React, { useState, useEffect } from 'react';
import axios from 'axios';

// The main component for our application, adapted for web preview
export default function App() {
  // State for the simulated barcode data
  const [barcodeInput, setBarcodeInput] = useState('');
  // State to track if a barcode has been "scanned"
  const [scanned, setScanned] = useState(false);
  // State to store the data from the last scan
  const [scannedData, setScannedData] = useState(null);

  // --- Event Handlers ---

  /**
   * This function simulates a barcode scan using the input field data.
   */
  const handleSimulateScan = () => {
    if (!barcodeInput) {
        alert('Please enter data into the text field to simulate a scan.');
        return;
    }
    // In a real app, the type would come from the scanner library
    const type = 'Simulated-Barcode'; 
    const data = barcodeInput;

    setScanned(true);
    setScannedData({ type, data });
    alert(`Simulated scan with type ${type} and data ${data}!`);
  };

  /**
   * Sends an HTTP GET request to a sample API using the scanned data.
   */
  const sendGetRequest = async () => {
    if (!scannedData) return;
    try {
      // Replace with your actual API endpoint
      const API_ENDPOINT = `https://api.example.com/data?barcode=${scannedData.data}`;
      console.log(`Sending GET request to: ${API_ENDPOINT}`);

      const response = await axios.get(API_ENDPOINT);

      console.log('GET Response:', response.data);
      alert('GET Request Successful!\nCheck the console for the response.');
    } catch (error) {
      console.error('Error sending GET request:', error);
      alert('Failed to send GET request. See console for details.');
    }
  };

  /**
   * Sends an HTTP POST request to a sample API with the scanned data in the body.
   */
  const sendPostRequest = async () => {
    if (!scannedData) return;
    try {
      // Replace with your actual API endpoint
      const API_ENDPOINT = 'https://api.example.com/data';
      const postData = {
        type: scannedData.type,
        data: scannedData.data,
        timestamp: new Date().toISOString(),
      };
      console.log(`Sending POST request to: ${API_ENDPOINT} with data:`, postData);
      
      const response = await axios.post(API_ENDPOINT, postData);

      console.log('POST Response:', response.data);
      alert('POST Request Successful!\nCheck the console for the response.');
    } catch (error) {
      console.error('Error sending POST request:', error);
      alert('Failed to send POST request. See console for details.');
    }
  };

  // --- Render Logic ---

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Barcode Scanner (Web Simulation)</h1>
      <p style={styles.description}>
        Since this is a web preview, we can't use the camera. 
        Enter barcode data below and click "Simulate Scan" to test the logic.
      </p>
      
      {!scanned && (
        <div style={styles.inputContainer}>
            <input
                type="text"
                value={barcodeInput}
                onChange={(e) => setBarcodeInput(e.target.value)}
                placeholder="Enter barcode data here"
                style={styles.input}
            />
            <button onClick={handleSimulateScan} style={styles.button}>Simulate Scan</button>
        </div>
      )}
      
      {/* Show buttons only after a barcode has been "scanned" */}
      {scanned && (
        <div style={styles.scanResultContainer}>
          <p style={styles.resultText}>Scanned Data: {scannedData?.data}</p>
          <div style={styles.buttonGroup}>
              <button onClick={sendGetRequest} style={styles.button}>Send GET Request</button>
              <button onClick={sendPostRequest} style={styles.button}>Send POST Request</button>
          </div>
          <button onClick={() => {
              setScanned(false);
              setScannedData(null);
              setBarcodeInput('');
          }} style={styles.button}>
            Scan Again
          </button>
        </div>
      )}
    </div>
  );
}

// --- Styles (Using JS objects for inline styling in React) ---

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f0f4f7',
    padding: '20px',
    fontFamily: 'sans-serif',
    height: '100vh',
    boxSizing: 'border-box'
  },
  title: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '10px',
    color: '#333',
  },
  description: {
    fontSize: '16px',
    marginBottom: '20px',
    color: '#555',
    textAlign: 'center',
    maxWidth: '400px'
  },
  inputContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '100%',
    maxWidth: '350px',
  },
  input: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
    fontSize: '16px',
    boxSizing: 'border-box'
  },
  scanResultContainer: {
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '10px',
    alignItems: 'center',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
    gap: '15px'
  },
  resultText: {
    fontSize: '16px',
    fontWeight: 'bold',
    marginBottom: '0px',
  },
  buttonGroup: {
    display: 'flex',
    justifyContent: 'space-around',
    width: '100%',
    gap: '10px'
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    color: 'white',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer'
  }
};
