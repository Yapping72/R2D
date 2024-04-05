import React, { createContext, useState, useContext } from 'react';
import { DismissibleAlert } from './DismissibleAlert';

// Create a Context for the alert system to be accessible throughout the component hierarchy
const AlertContext = createContext();

/*
* Import this useAlert() function to retrieve the Alert context
*/
export const useAlert = () => {
  return useContext(AlertContext);
};

/**
 * To create an alert, the component has to import useAlert, 
 * to render the alert the component needs to invoke the showAlert('serverity', 'message')
 */
export const AlertProvider = ({ children }) => {
  const [alert, setAlert] = useState(null);


/**
 * Renders a DismissibleAlert component
 * @param {string} severity -  Accepts one of 'error', 'warning', 'info', or 'success' 
 * @param {string} message - The message text to display inside the alert.
 * @returns Displays the DismissibleAlert
 */
  const showAlert = (severity, message) => {
    setAlert({ severity, message });
    setTimeout(() => {
      setAlert(null);
    }, 8000); // Duration in ms to display alert 
  };

  return (
    <AlertContext.Provider value={{ showAlert }}>
      {alert && <DismissibleAlert severity={alert.severity} message={alert.message} />}
      {children}
    </AlertContext.Provider>
  );
};
