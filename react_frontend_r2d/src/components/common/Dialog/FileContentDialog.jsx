import React from 'react';
import { Dialog, DialogActions, DialogContent, Button, Box, Typography } from '@mui/material';
import ReadOnlyEditor from '../Tables/ReadOnlyEditor';

const FileContentDialog = ({ open, onClose, fileContent, fileMetadata }) => {
  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      aria-labelledby="file-content-title"
    >
      <DialogContent>
        <Box sx={{width:"30vw", height:"45vh", overflow:"hidden"}}>
          <Typography variant="h6" sx={{textAlign:"center"}}>{fileMetadata.filename}</Typography>
          <hr></hr>
          <ReadOnlyEditor fileExtension={fileMetadata.type} fileContents={fileContent}></ReadOnlyEditor>
          <hr></hr>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default FileContentDialog;
