import React, { createContext, useState, useContext } from 'react';
import { DismissibleAlert } from './DismissibleAlert';

// Create a Context for the alert system to be accessible throughout the component hierarchy
const AlertContext = createContext();

export const useAlert = () => {
  return useContext(AlertContext);
};

export const AlertProvider = ({ children }) => {
  const [alert, setAlert] = useState(null);

  const showAlert = (severity, message) => {
    setAlert({ severity, message });
    setTimeout(() => {
      setAlert(null);
    }, 5000); // Duration in ms to display alert
  };

  return (
    <AlertContext.Provider value={{ showAlert }}>
      {alert && <DismissibleAlert severity={alert.severity} message={alert.message} />}
      {children}
    </AlertContext.Provider>
  );
};
