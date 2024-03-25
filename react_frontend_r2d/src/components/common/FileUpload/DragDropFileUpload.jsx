import React from 'react';
import { Button, Container, Tooltip, Typography } from "@mui/material";
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import './DragDropFileUpload.css'
import { useAlert } from '../Alerts/AlertContext';

/*
* Component that supports uploading of files via Drag and Drop or Click features.
* When a file dropped in, validation is performed, if all validation passes, file is stored in IndexedDb.
*/
const DragDropFile = ({ title = "Drag and drop files here", validator, repository }) => {
  const [dragActive, setDragActive] = React.useState(false);
  const inputRef = React.useRef(null);
  const { showAlert } = useAlert();

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

  // Retrieves the list of supported file types passed to the validator
  const getSupportedFileTypes = () => {
    return validator.getValidExtensions();
  };
  // Retrieves the max size that the validator supports
  const getSupportedMaxSize = () => {
    return validator.getMaxFileSize();
  }
  // Prettifies the output for max file size
  const formatFileSize = (decimalPoints = 2) => {
    let bytes = getSupportedMaxSize();
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimalPoints < 0 ? 0 : decimalPoints;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }
  // Returns the maximum number of lines the validator accepts
  const getSupportedMaxLines = () => {
    return validator.getMaxLineCount();
  }
  // Performs validation on the list of users uploaded files
  const processFiles = (files) => {
    Array.from(files).forEach(async (file) => {
      try {
        const validationResult = await validator.validate(file);
        if (validationResult.result === 'success') {
          // Success: Store the file into db
          //console.log("Success:", validationResult);
          repository.handleWriteFileAndMetadataToDB(file, validationResult.file_metadata);
          showAlert('success', `${validationResult.file_metadata.filename} has been uploaded successfully.`)
        } else {
          // Failure: log the message and alert the user
          showAlert('error', `${validationResult.file_metadata.filename} could not be uploaded. Please check that the file meets uploading requirements.`)
        }
      } catch (error) {
        // Handle FileReader errors
        console.error("Error encountered while uploading file in Visualize Page: ", error);
        showAlert('error', `We encountered an issue while uploading ${validationResult.file_metadata.filename}. Please try again later.`)
      } finally {
        // Reset the input value
        if (inputRef.current) {
          inputRef.current.value = '';
        }
      }
    });
  };

  return (
    <Container className="drag-drop-container">
      <Tooltip title="Drag and drop files or click to select file to upload">
        <form className="form-file-upload" onDragEnter={handleDragEnter} onDragOver={handleDragOver} onDragLeave={handleDragLeave} onDrop={handleDrop}>
          <input ref={inputRef} type="file" id="input-file-upload" multiple={true} onChange={handleChange} className="input-file-upload" />
          <label htmlFor="input-file-upload" className={`label-file-upload ${dragActive ? "drag-active" : ""}`}>
            <Button className="upload-button" onClick={() => inputRef.current.click()}>
              <CloudUploadIcon className="cloud-upload-icon" sx={{ fontSize: "100px", color: "light-blue" }} />
            </Button>
            <Typography variant="h5" className="upload-instructions">
              {title}
            </Typography>
            <Typography className="supported-file-types">
              <ul>
                <li>Files cannot not be larger than <b>{formatFileSize()}</b></li>
                <li>Supported file types: <b>{getSupportedFileTypes()}</b></li>
                <li>Files must not contain more than <b>{getSupportedMaxLines()} lines</b></li>
              </ul>
            </Typography>
          </label>
        </form>
      </Tooltip>
    </Container>
  );
};

export default DragDropFile;