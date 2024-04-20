import React, { createContext, useState, useContext, useRef, useEffect } from 'react';
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
  const alertRef = useRef(null);  // Create a ref for the alert component
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
    }, 5000); // Duration in ms to display alert 
  };
  // Use effect to scroll to the alert when it is displayed
  useEffect(() => {
    if (alert && alertRef.current) {
      alertRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }, [alert]); // Dependency on alert, runs when it changes

  const onClose = () => {
    setAlert(null);
  }

  return (
    <AlertContext.Provider value={{ showAlert }}>
      {alert && <DismissibleAlert severity={alert.severity} message={alert.message} onClose={onClose} ref={alertRef} />}
      {children}
    </AlertContext.Provider>
  );
};
