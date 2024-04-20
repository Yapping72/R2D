import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

// Add pages here
import Layout from './components/common/Layout/Layout.jsx';
import HomePage from './pages/Home/HomePage.jsx';
import AnalyzePage from './pages/Analyze/AnalyzePage.jsx';
import UploadRequirementsPage from './pages/UploadRequirements/UploadRequirementsPage.jsx';
import VisualizePage from './pages/Visualize/VisualizePage.jsx';
import AccountPortalPage from './pages/AccountPortal/AccountPortal.jsx';
import { AlertProvider } from './components/common/Alerts/AlertContext.jsx';

function App() {
  const theme = createTheme({
    palette: {
      mode: 'dark', // Set theme mode to dark
      background: {
        default: '#000000', // Fully black background
      },
    },
    typography: {
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif', 
      fontSize: 16, 
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline /> 
      <Router>
      <div id="root">
        <div className="main-content">
          <main>
            <Routes>
            <Route path="/" element={<Layout><HomePage /></Layout>} />
            <Route path="/home" element={<Layout><HomePage /></Layout>} />
            <Route path="/analyze" element={<Layout><AnalyzePage /></Layout>} />
            <Route path="/upload" element={<Layout><UploadRequirementsPage /></Layout>} />
            <Route path="/visualize" element={<Layout><VisualizePage /></Layout>} />
            <Route path="/account-portal" element={<Layout><AccountPortalPage /></Layout>} />
            </Routes>
          </main>
        </div>
      </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
