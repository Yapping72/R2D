import {useState } from 'react';
import { Box, Typography, Container, Tab, Tabs, Divider, Button } from "@mui/material";
import UserStoryManagementModal from '../../components/common/UserStory/UserStoryManagementModal';
import UserStoryTable from '../../components/common/UserStory/UserStoryTable';
import FeatureVisualizer from '../../components/common/UserStory/FeatureVisualizer';
import { UserStoryContextProvider } from '../../components/common/UserStory/UserStoryContextProvider';
import FileReaderUtility from '../../utils/FileHandling/FileReaderUtility';
import { UserStoryFileRepository } from '../../utils/Repository/UserStoryFileRepository';
import { useAlert } from '../../components/common/Alerts/AlertContext';

/**
 * The `UploadRequirementsPage` is responsible for managing the upload and visualization
 * of user stories from files. It allows users to upload files, select files for viewing,
 * and manage user stories within those files through a tabbed interface.
 *
 * It uses a context provider to manage operations like add, edit, and delete of user stories.
 * Each operation updates the files' data which is then reflected in the visual components.
 *
 * State:
 * - `value`: Controls the active tab.
 * - `filesData`: Maintains an array of file data including featureData and fileId.
 */

const UploadRequirementsPage = () => {
    const { showAlert } = useAlert();
    const [value, setValue] = useState(0); // Tab Value
    const [filesData, setFilesData] = useState([]);
    
    const handleRemoveSelectedFile = async (index) => {
         // Create a new array by filtering out the element at the specific index
        const updatedFilesData = filesData.filter((item, i) => i !== index);
        // Update the state with the new array
        setFilesData(updatedFilesData);
    }

    const handleTabChange = (event, newValue) => {
        setValue(newValue);
    };

    /**
     * Handles the upload of files, parsing the contents and storing them with their respective fileId.
     * This parsed data is then used to populate the user stories visualized in the FeatureVisualizer.
     * @param {File} file - The file uploaded by the user.
     * @param {Object} fileMetadata - Metadata containing the fileId.
     */
    const handleFileUpload = async (file, fileMetadata) => {
        try {
            const fileContents = await FileReaderUtility.readAsText(file);
            const jsonFileContents = JSON.parse(fileContents);
            setFilesData(prevFilesData => [
                ...prevFilesData,
                { featureData: jsonFileContents, fileId: fileMetadata.id, fileMetadata: fileMetadata}
            ]);
            setValue(1); // Switch to the tab showing the grids
        } catch (error) {
            console.error('Error rendering the uploaded file', error);
            showAlert("error", "Error rendering the uploaded file");
        }
    };

    /**
     * Handles the selection of files, updating the state with the selected file's data.
     * This allows the FeatureVisualizer to display the selected file's user stories.
     * @param {string} fileContents - The contents of the selected file.
     * @param {Object} fileMetadata - Metadata containing the fileId.
     */
    const handleFileSelection = async (fileContents, fileMetadata) => {
        try {
            const jsonFileContents = JSON.parse(fileContents);
            setFilesData(prevFilesData => [
                ...prevFilesData,
                { featureData: jsonFileContents, fileId: fileMetadata.id, fileMetadata: fileMetadata}
            ]);
            setValue(1);
        } catch (error) {
            console.error('Error processing the selected file', error);
            showAlert("error", "Error processing the selected file");
        }
    };

    /**
     * Invoked when a user story is edited. Updates the specific user story by fileId and recordId,
     * ensuring the changes are reflected across the application.
     * @param {string} fileId - The ID of the file the user story belongs to.
     * @param {string} recordId - The specific ID of the user story within the file.
     * @param {Object} editedData - The updated data for the user story.
     */
    const handleRequirementsEdit = async (fileId, recordId, editedData) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.updateRecordInFile(fileId = fileId, recordId = recordId, editedData = editedData)
            if (result.success) {
                showAlert("success", "User story updated");
                const updatedFeatures = await repository.getFeaturesFromFile(fileId)
                // Update the existing file content state
                setFilesData(prevFilesData => prevFilesData.map(fileData =>
                    fileData.fileId === fileId
                        ? { ...fileData, featureData: updatedFeatures.data } 
                        : fileData 
                ));
            }
        }
        catch (error) {
            console.error("Error encountered while trying to edit user story:", error);
            showAlert("error", "Failed to update user story please try again");
        }
    };

    /**
     * Handles adding new user stories to a file. Fetches and updates the relevant file data on success.
     * @param {string} fileId - The ID of the file to add the new user story.
     * @param {Object} newData - The data for the new user story to be added.
     */
    const handleRequirementsAdd = async (fileId, newData) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.addRecordToFile(fileId = fileId, newData = newData);
            if (result.success) {
                showAlert("success", `User story saved to file id: ${fileId}`);
                // Get the updated file contents
                const updatedFeatures = await repository.getFeaturesFromFile(fileId)
                // Update the existing file content state
                setFilesData(prevFilesData => prevFilesData.map(fileData =>
                    fileData.fileId === fileId
                        ? { ...fileData, featureData: updatedFeatures.data } 
                        : fileData 
                ));
            }
            else {
                showAlert("error",  `Failed to add user story to file id: ${fileId}`);
            }
        }
        catch (error) {
            console.error("Error encountered while trying to add user story:", error);
            showAlert("error", "Failed to add user story please try again");
        }
    }

    /**
     * Handles the deletion of user stories from a file. Updates the file's data in the state upon successful deletion.
     * @param {string} fileId - The ID of the file from which the user story is being deleted.
     * @param {string} recordId - The ID of the user story to be deleted.
     */
    const handleRequirementsDelete = async (fileId, recordId) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.deleteRecordInFile(fileId = fileId, recordId = recordId);
            if (result.success) {
                showAlert("success", "User story deleted");
                // Get the updated file contents
                const updatedFeatures = await repository.getFeaturesFromFile(fileId)
                // Update the existing file content state
                setFilesData(prevFilesData => prevFilesData.map(fileData =>
                    fileData.fileId === fileId
                        ? { ...fileData, featureData: updatedFeatures.data } 
                        : fileData 
                ));
             
            }
            else {
                showAlert("error",  `Failed to deleted user story from file ${fileId}`);
            }
        }
        catch (error) {
            console.error("Error encountered while trying to delete user story", error)
            showAlert("error", "Failed to delete user story please try again");
        }
    }

    const handleUserStorySubmit = async (result) => {
        if (result.success) {
            showAlert("success", "Job successfully added to queue.");
            // Redirect to analysis page (TBC)
        } 
        else {
            showAlert("error",  `Failed to add job to queue.`);
        }

    }

    return (
        <UserStoryContextProvider
            handleFileUpload={handleFileUpload}
            handleFileSelection={handleFileSelection}
            handleRequirementsEdit={handleRequirementsEdit}
            handleRequirementsAdd={handleRequirementsAdd}
            handleRequirementsDelete={handleRequirementsDelete}>
            <Container>
                <Typography variant='h3'>User Story Uploader</Typography>
                <Box >
                    <Tabs value={value} onChange={handleTabChange} aria-label="basic tabs example">
                        <Tab label="Upload & Select User Stories" />
                        <Tab label="Feature Visualizer" />
                    </Tabs>
                    <Divider sx={{ my: 2 }} /> 
                </Box>
                {value === 0 && (
                    <Box>
                        <UserStoryManagementModal />
                        <Divider sx={{ my: 2 }} /> 
                        <UserStoryTable />
                    </Box>
                )}
                {value === 1 && (
                    <Box>
                        <FeatureVisualizer filesData={filesData} handleRemoveSelectedFile={handleRemoveSelectedFile} handleUserStorySubmit={handleUserStorySubmit}/>
                    </Box>
                )}
            </Container>
        </UserStoryContextProvider>
    )
}

export default UploadRequirementsPage