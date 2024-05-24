import React, {useEffect} from 'react';
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
/**
 * Renders a backdrop that disappears after X-milliseconds
 * @param {duration} int Duration in milliseconds for the backdrop to be displayed
 * @param {function} onClose Callback function to close the backdrop
 * @returns {Backdrop} Backdrop with a circular progress bar that is displayed for a specified duration
 */
const TimedBackdrop = ({ duration = 1000, open, onClose }) => {
    useEffect(() => {
        if (open) {
            const timer = setTimeout(() => {
                onClose();
            }, duration);
            return () => clearTimeout(timer);
        }
    }, [open, duration, onClose]);

    return (
        <Backdrop
            sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
            open={open}
        >
            <CircularProgress color="inherit" />
        </Backdrop>
    );
};

export default TimedBackdrop;