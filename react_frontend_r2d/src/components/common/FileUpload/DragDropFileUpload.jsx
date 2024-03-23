import React from 'react';
import { Box, Button, Container, Tooltip, Typography} from "@mui/material";
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import FileUploadValidator from '../../../utils/FileUploadValidator';
import R2DModal from '../Modals/R2DModal'
import './DragDropFileUpload.css'

const DragDropFile = ({ title = "Upload your files here" }) => {
  const [dragActive, setDragActive] = React.useState(false);
  const inputRef = React.useRef(null);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    alert(`Validating: ${file.name}`);
    processFiles(e.dataTransfer.files);
  };

  const handleChange = (e) => {
    e.preventDefault();
    processFiles(e.target.files);
  };

  const processFiles = (files) => {
    Array.from(files).forEach(async (file) => {
      try {
        const validationResult = await FileUploadValidator.validate(file);
        if (validationResult.result === 'success') {
          // Success: perform the action with the file, e.g., uploading
          console.log("Success:", validationResult);
          alert(`Success: ${validationResult.file_metadata.filename}`);
        } else {
          // Failure: log the message and alert the user
          console.error("Validation failed:", validationResult.message);
          alert(`Validation failed: ${validationResult.message}`);
        }
      } catch (error) {
        // Handle FileReader errors
        console.error("Error reading file:", error);
        alert("Error reading file. Please try again.");
      }
    });
  };

  return (
    <R2DModal>
      <Container className="drag-drop-container">
        <Tooltip title="Drag and drop files or click to select file to upload">
          <form className="form-file-upload" onDragEnter={handleDragEnter} onDragOver={handleDragOver} onDragLeave={handleDragLeave} onDrop={handleDrop}>
            <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} className="input-file-upload" />
            <label htmlFor="input-file-upload" className={`label-file-upload ${dragActive ? "drag-active" : ""}`}>
              <Button className="upload-button" onClick={() => inputRef.current.click()}>
                <CloudUploadIcon />
              </Button>
              <Typography variant="h5" className="upload-instructions">
                Drag and drop files here
              </Typography>
              <Typography className="supported-file-types">
                <ul>
                <li>Files Must not be larger than 15mb</li>
                <li>Supported File Types: .txt, .json, .mermaid</li>
                </ul>
              </Typography>
            </label>
          </form>
        </Tooltip>
      </Container>
    </R2DModal>
  );
};

export default DragDropFile;