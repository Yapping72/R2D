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
import ErrorPage from './pages/ErrorPage/ErrorPage.jsx';
import { ROUTES } from './utils/Pages/RoutesConfig.jsx';

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
            <Route path={ROUTES.BASE} element={<Layout><HomePage /></Layout>} />
            <Route path={ROUTES.HOME} element={<Layout><HomePage /></Layout>} />
            <Route path={ROUTES.ANALYZE} element={<Layout><AnalyzePage /></Layout>} />
            <Route path={ROUTES.UPLOAD} element={<Layout><UploadRequirementsPage /></Layout>} />
            <Route path={ROUTES.VISUALIZE} element={<Layout><VisualizePage /></Layout>} />
            <Route path={ROUTES.ACCOUNT_PORTAL} element={<Layout><AccountPortalPage /></Layout>} />
            <Route path={ROUTES.ERROR} element={<Layout><ErrorPage /></Layout>} />  
            </Routes>
          </main>
        </div>
      </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
