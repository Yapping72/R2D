import React, { useState, useEffect } from 'react';
import Alert from '@mui/material/Alert';


/**
 * DismissibleAlert is a component that displays an alert message on the screen.
 * The alert will automatically dismiss after a set amount of time (8 seconds).
 *
 * @param {string} severity - The severity level of the alert which determines the color and icon.
 *                            Accepts one of 'error', 'warning', 'info', or 'success'.
 * @param {string} message - The message text to display inside the alert.
 * @returns A Material-UI Alert component configured to be dismissible after 5 seconds.
 *
 * Note: This component is typically used in conjunction with AlertContext, which manages
 * the display and state of alerts throughout the application. The showAlert function provided
 * by AlertContext can be used to display the alert with a specified severity and message.
 */

const DismissibleAlert = React.forwardRef(({ severity, message, onClose }, ref) => {
    return (
        <Alert variant="filled" severity={severity} onClose={onClose} ref={ref}>
            {message}
        </Alert>
    );
});
export { DismissibleAlert }; 
