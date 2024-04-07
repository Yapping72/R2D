import React, { useState } from 'react';
import { Typography, Modal, Box, Button } from '@mui/material';

// Adjust your style object to center the Box within the modal
const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '40%', // Adjust the width as per your need
  height: '55%', // Adjust the height as per your need
  bgcolor: 'background.paper', // Change this to match your theme's color or make it transparent
  boxShadow: 24,
};
/**
 * Button excepts either a title, a icon or both
 * @param {string} title - Title that will be displayed on the button to open the modal
 * @param {icon} icon - MUI icon to be displayed on the button 
 * @returns 
 */
const R2DModal = ({children, title="R2DModal", icon=null}) => {
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <>
      <Button variant="outlined" onClick={handleOpen} startIcon={icon}>
      {title && <Typography>{title}</Typography>}
      </Button>
      <Modal open={open} onClose={handleClose} aria-labelledby="modal-modal-title" aria-describedby="modal-modal-description">
        <Box sx={style}>
        {children}
        </Box>
    </Modal>
    </>
  );
};

export default R2DModal;
