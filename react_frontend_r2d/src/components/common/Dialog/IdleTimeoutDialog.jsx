import React, { useState, useEffect, useRef } from 'react';
import {Dialog, DialogTitle, DialogContent, DialogActions, Typography, Button, Box, Stack } from '@mui/material';
import './IdleTimerDialog.css'; // Import the CSS file for animations
import { useAuth } from '../Authentication/AuthContext';

const IdleTimeoutDialog = () => {
    const { showDialog, setShowDialog, remainingTime, handleStayLoggedIn, logout } = useAuth();
    const [minutes, setMinutes] = useState(0);
    const [seconds, setSeconds] = useState(0);
    
    const handleLoginButtonClick = () => {
        setShowDialog(false);
        handleStayLoggedIn();
    }

    useEffect(() => {
        // Convert remaining time to minutes and seconds whenever remainingTime changes
        const mins = Math.floor(remainingTime / 60);
        const secs = remainingTime % 60;
        setMinutes(mins);
        setSeconds(secs);

        if (secs === 0 && mins === 0) {
            // Logout action is handled by the useIdleTimeout onIdle hence not invoked here.
            setShowDialog(false);
        }
    }, [remainingTime]);

    const handleLogOut = () => {
        setShowDialog(false);
        console.debug("User selected to logout. Logging out.");
        logout();
    };

    return (
        <Dialog
            open={showDialog}
            onClose={handleLoginButtonClick}
            aria-labelledby="idle-timeout-warning"
            aria-describedby="idle-timeout-warning-description"
            className="idle-timeout-dialog"
            maxWidth="sm"
            fullWidth
            sx={{ borderRadius: 2, overflow: 'hidden' }}
        >
            <DialogTitle id="idle-timeout-warning">
                <Box display="flex">
                    <Typography variant="h6" component="span" className="dialog-title">
                        Are you still here?
                    </Typography>
                </Box>
            </DialogTitle>
            <DialogContent sx={{ overflow: 'hidden' }}>
                <Stack spacing={2} alignItems="center" justifyContent="center">
                    <Typography id="idle-timeout-warning-description" className="dialog-description">
                        We detected that you have been idle for extended periods. To protect your account, you will be automatically logged out once the timer reaches 0.
                    </Typography>
                    <Box display="flex" alignItems="center" justifyContent="center" style={{ marginTop: '16px' }}>
                        <div className="clock">
                            <div className="cup top">
                                <div className="sand delayed"></div>
                            </div>
                            <div className="cup">
                                <div className="sand"></div>
                            </div>
                        </div>
                        <Typography
                            variant="h4"
                            component="span"
                            className="pulsating-text"
                            style={{ marginLeft: '16px' }} // Add margin to align the text
                        >
                            {minutes}:{seconds < 10 ? `0${seconds}` : seconds}
                        </Typography>
                    </Box>
                </Stack>
            </DialogContent>
            <DialogActions>
                <Box display="flex" justifyContent="space-between" width="100%">
                    <Button variant="outlined" color="primary" onClick={handleLogOut} className="dialog-button">
                        Logout
                    </Button>
                    <Button variant="outlined" color="primary" onClick={handleStayLoggedIn} className="dialog-button">
                        Stay Logged In
                    </Button>
                </Box>
            </DialogActions>
        </Dialog>
    );
};


export default IdleTimeoutDialog;