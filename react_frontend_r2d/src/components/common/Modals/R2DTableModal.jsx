import React, { useState } from 'react';
import { Typography, Modal, Box, Button } from '@mui/material';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  border: '1px solid',
  bgcolor: 'transparent', 
  boxShadow: 24,
  maxHeight: '85vh',
  maxWidth: '95vw',
  overflow: 'auto'
};

/**
 * Button excepts either a title, a icon or both
 * @param {string} title - Title that will be displayed on the button to open the modal, Modal displayed takes up 80% viewport width
 * @param {icon} icon - MUI icon to be displayed on the button 
 * @returns 
 */
const R2DTableModal = ({children, title="R2DTableModal", icon=null}) => {
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <>
      <Button 
      variant="outlined" 
      onClick={handleOpen} 
      startIcon={icon}>
      {title && <Typography variant='p'>{title}</Typography>}
      </Button>
      <Modal 
      open={open} 
      onClose={handleClose} 
      aria-labelledby="modal-modal-title" 
      aria-describedby="modal-modal-description">
        <Box sx={style}>
        {children}
        </Box>
    </Modal>
    </>
  );
};

export default R2DTableModal;
