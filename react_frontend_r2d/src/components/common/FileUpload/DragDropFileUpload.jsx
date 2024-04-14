import React from 'react';
import { Button, Container, Tooltip, Typography } from "@mui/material";
import FileUploadIcon from '@mui/icons-material/FileUpload';
import './DragDropFileUpload.css'
import { useAlert } from '../Alerts/AlertContext';

/**
 * A drag-and-drop file upload component. It supports uploading files by either dragging them into
 * the drop zone or clicking to select files. The component validates files against provided criteria
 * and stores valid files using the provided repository.
 * 
 * Props:
 * - title: Display text for the upload area. Default is "Drag and drop files here".
 * - validator: An object that provides file validation methods.
 * - repository: An object for storing valid files, expected to have a method for writing files and their metadata to a database.
 * - handleFileUpload: A callback function that is invoked after a file passes validation and is stored.
 * - IconComponent: A React component to be used as the upload icon. Default is FileUploadIcon from MUI.
 * - handleFilePreProcessing: Optional function that will be invoked to do preprocessing actions e.g., adding record identifiers to requirements 
 * 
 * The `validator` prop must provide:
 *   - getValidExtensions(): Returns an array of supported file extensions.
 *   - getMaxFileSize(): Returns the maximum file size in bytes.
 *   - validate(file): Returns a promise that resolves with a validation result object.
 *   - getMaxLineCount(): Returns the maximum number of lines allowed in a file.
 * 
 * The `repository` prop must provide:
 *   - handleWriteFileAndMetadataToDB(file, metadata): Stores the file and its metadata.
 */

const DragDropFile = ({ 
  title = "Drag and drop files here", 
  validator, 
  repository, 
  handleFileUpload = () => {}, 
  handleFilePreProcessing = (file) => {return file},
  IconComponent=FileUploadIcon}) => {

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
          // Success: Store the file into db, append the generated id to filemetadata
          let processed_file = await handleFilePreProcessing(file); // Optionally perform any preprocessing as required
          const result = await repository.handleWriteFileAndMetadataToDB(processed_file, validationResult.file_metadata);
          validationResult.file_metadata.id = result.data.id
          showAlert('success', `Your file ${validationResult.file_metadata.filename} has been uploaded successfully.`)
          // Returns the file to the callback function
          handleFileUpload(processed_file, validationResult.file_metadata); 
        } else {
          // Failure: log the message and alert the user
          showAlert('error', `Your file could not be uploaded. Please check that the file meets uploading requirements.`)
        }
      } catch (error) {
        // Handle FileReader errors
        console.error("Error encountered while uploading file in Visualize Page: ", error);
        showAlert('error', `We encountered an issue while uploading your file. Please try again later.`)
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
              <IconComponent className="cloud-upload-icon" sx={{ fontSize: "100px", color: "light-blue" }} />
            </Button>
            <Typography variant="h5" className="upload-instructions">
              {title}
            </Typography>
            <Typography component="div" className="supported-file-types">
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