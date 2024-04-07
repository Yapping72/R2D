import React from 'react';
import { Dialog, DialogActions, DialogContent, Button, Box, Typography } from '@mui/material';
import ReadOnlyEditor from '../Tables/ReadOnlyEditor';


/**
 * Dialog component to display the content of a Mermaid file and allow selection.
 * This component expects to receive a `handleFileSelection` function,
 * typically from the MermaidContext, to handle the selection of file content.
 * 
 * @param {Object} props - Props for configuring the dialog.
 * @param {boolean} props.open - Controls the visibility of the dialog.
 * @param {Function} props.onClose - Callback to invoke when closing the dialog.
 * @param {string} props.fileContent - The content of the file to display.
 * @param {Object} props.fileMetadata - Metadata about the file, including filename and type.
 * @param {Function} props.handleFileSelection - Callback to invoke when a file is selected
 */

const FileContentDialog = ({ open, onClose, fileContent, fileMetadata, handleFileSelection}) => {
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
        {handleFileSelection && (
            <Button onClick={() => handleFileSelection(fileContent)}>Select</Button>
          )}
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default FileContentDialog;
