import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import HomePage from './pages/Home/HomePage.jsx';
import AnalyzePage from './pages/Analyze/AnalyzePage.jsx';
import UploadRequirementsPage from './pages/UploadRequirements/UploadRequirementsPage.jsx';
import Layout from './components/common/Layout/Layout.jsx';
import VisualizePage from './pages/Visualize/VisualizePage.jsx';

function App() {
  const theme = createTheme({
    palette: {
      mode: 'dark', // Set theme mode to dark
    },
    typography: {
      fontFamily: 'Roboto, sans-serif', 
      fontSize: 16, 
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Applies global styles and resets */}
      <Router>
      <div id="root">
        <div className="main-content">
          <main>
          <Routes>
            <Route path="/" element={<Layout><HomePage /></Layout>} />
            <Route path="/analyze" element={<Layout><AnalyzePage /></Layout>} />
            <Route path="/upload" element={<Layout><UploadRequirementsPage /></Layout>} />
            <Route path="/visualize" element={<Layout><VisualizePage /></Layout>} />
          </Routes>
          </main>
        </div>
      </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
