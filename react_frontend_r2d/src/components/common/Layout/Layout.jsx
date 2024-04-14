import React from 'react';
import Header from "../Header/Header.jsx";
import Footer from "../Footer/Footer.jsx";
import {Container, Box} from "@mui/material";
import { AlertProvider } from '../Alerts/AlertContext.jsx';
const Layout = ({ children }) => {
  return (
    <Box sx={{
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100vh', // full height of the viewport
    }}>
      <Header />
      <Container disableGutters maxWidth={false} sx={{
        flexGrow: 1, // container takes up all available space
        p: 1, // padding inside the container
        width: '95%', // full width of the parent
      }}>
      <AlertProvider>
        {children}
      </AlertProvider>
      </Container>
      <Footer />
    </Box>
  );
};

export default Layout;