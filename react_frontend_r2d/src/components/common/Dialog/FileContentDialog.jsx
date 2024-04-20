import React from 'react';
import { Dialog, DialogActions, DialogContent, Button, Box, Typography, Divider } from '@mui/material';
import ReadOnlyEditor from '../Tables/ReadOnlyEditor';
import FileDownloadUtility from '../../../utils/FileHandling/FileDownloaderUtility';

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

const FileContentDialog = ({ 
  open, 
  onClose, 
  fileContent, 
  fileMetadata, 
  handleFileSelection}) => {
  
  // Triggers the handleFileSelection function and also closes the dialog.
  const handleSelectAndClose = () => {
    if(handleFileSelection) {
      handleFileSelection(fileContent, fileMetadata);
    }
    onClose()
  };

  const handleDownload = (fileContent, fileMetadata) => {
    console.log(fileMetadata)
    switch (fileMetadata.type) {
      case 'application/json':
        FileDownloadUtility.downloadJson(fileContent, fileMetadata.filename);
        break;
      case 'text/plain':
        FileDownloadUtility.downloadTxt(fileContent, fileMetadata.filename);
        break;
      case 'text/markdown':
        FileDownloadUtility.downloadMd(fileContent,fileMetadata.filename);
        break;
      default:
        console.error('Unsupported file type');
    }
  }

  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      aria-labelledby="file-content-title"
      
      PaperProps={{
        sx:{
          backgroundColor: "black", // Ensures the background color is black
          color: "#FFFFFF", // Optional: setting text color to white for better contrast\
          }
      }}
    >
      <DialogContent>
        <Box sx={{width:"40vw", height:"60vh", overflow:"hidden"}}>
          <Typography variant="h6" sx={{textAlign:"center"}}>{fileMetadata.filename}</Typography>
          <Divider sx={{my:1}}></Divider>
          <ReadOnlyEditor fileExtension={fileMetadata.type} fileContents={fileContent}></ReadOnlyEditor>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => handleDownload(fileContent, fileMetadata)}>Download</Button>
        <Button onClick={handleSelectAndClose}>Select</Button>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default FileContentDialog;
