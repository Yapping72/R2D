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
import OTPPage from './pages/AccountPortal/OTPPage.jsx';
import LogoutPage from './pages/LogoutPage/LogoutPage.jsx';
import HistoryPage from './pages/HistoryPage/HistoryPage.jsx';

// Add providers, utils and other components here
import { ROUTES } from './utils/Pages/RoutesConfig.jsx';
import { AuthProvider } from './components/common/Authentication/AuthContext.jsx';

import ProtectedRoute from './components/common/Authentication/ProtectedRoutes.jsx';
import IdleTimeoutDialog from './components/common/Dialog/IdleTimeoutDialog.jsx';

function App() {
  const theme = createTheme({
    palette: {
      mode: 'dark', // Set theme mode to dark
      background: {
        default: '#000000', // Fully black background
      },
    },
    typography: {
      fontFamily: '"Roboto"',
      fontSize: 16,
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AuthProvider>
        <IdleTimeoutDialog/>
          <div id="root">
            <div className="main-content">
              <main>
                <Routes>
                  {/*Pages that dont require JWT*/}
                  <Route path={ROUTES.BASE} element={<Layout><HomePage /></Layout>} />
                  <Route path={ROUTES.HOME} element={<Layout><HomePage /></Layout>} />
                  <Route path={ROUTES.ACCOUNT_PORTAL} element={<Layout><AccountPortalPage /></Layout>} />
                  <Route path={ROUTES.OTP} element={<Layout><OTPPage /></Layout>} />
                  <Route path={ROUTES.VISUALIZE} element={<Layout><VisualizePage /></Layout>} />
                  <Route path={ROUTES.LOGOUT} element={<Layout><LogoutPage /></Layout>} />
                  <Route path={ROUTES.ERROR} element={<Layout><ErrorPage /></Layout>} />

                  {/*Pages that require users to be logged in*/}
                  <Route path={ROUTES.ANALYZE} element={<ProtectedRoute element={<Layout><AnalyzePage /></Layout>} />} />
                  <Route path={ROUTES.UPLOAD} element={<ProtectedRoute element={<Layout><UploadRequirementsPage /></Layout>} />} />
                  <Route path={ROUTES.HISTORY} element={<ProtectedRoute element={<Layout><HistoryPage /></Layout>} />} />
                </Routes>
              </main>
            </div>
          </div>
          
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;
