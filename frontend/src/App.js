import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import AnalyticsSummary from './components/AnalyticsSummary';
import ChartSection from './components/ChartSection';
import UserList from './components/UserList';

function App() {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    setAnalyticsData(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      console.log('Uploading file:', file.name, 'Size:', file.size);

      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      console.log('Response status:', response.status, response.statusText);

      if (!response.ok) {
        let errorMessage = 'Failed to analyze chat file';
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
        } catch (parseError) {
          // If response is not JSON, try to get text
          try {
            const errorText = await response.text();
            errorMessage = errorText || errorMessage;
          } catch (textError) {
            errorMessage = `Server error: ${response.status} ${response.statusText}`;
          }
        }
        throw new Error(errorMessage);
      }

      const result = await response.json();
      console.log('Upload successful, received data:', result);
      
      if (result.success && result.data) {
        setAnalyticsData(result.data);
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (err) {
      // Handle network errors
      if (err.message === 'Failed to fetch' || err.name === 'TypeError' || err.message.includes('NetworkError')) {
        setError('Unable to connect to the server. Please make sure the backend is running on http://localhost:8000');
      } else {
        setError(err.message || 'An error occurred while processing the file');
      }
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>WhatsApp Chat Analyzer</h1>
        <p>Upload your WhatsApp chat export to analyze group activity</p>
      </header>

      <main className="app-main">
        <FileUpload
          onFileUpload={handleFileUpload}
          loading={loading}
          error={error}
        />

        {analyticsData && (
          <>
            <AnalyticsSummary summary={analyticsData.summary} />
            <ChartSection dailyData={analyticsData.daily_data} />
            <UserList users={analyticsData.users_active_4plus_days} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
