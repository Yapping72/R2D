import { useEffect, useState } from 'react';
import { AlertProvider } from '../../components/common/Alerts/AlertContext';
import { Box, Typography, Container, Grid } from "@mui/material";
import UserStoryManagementModal from '../../components/common/UserStory/UserStoryManagementModal';
import UserStoryTable from '../../components/common/UserStory/UserStoryTable';
import FeatureVisualizer from '../../components/common/UserStory/FeatureVisualizer';
import { UserStoryContextProvider } from '../../components/common/UserStory/UserStoryContextProvider';
import FileReaderUtility from '../../utils/FileHandling/FileReaderUtility';
import { UserStoryFileRepository } from '../../utils/Repository/UserStoryFileRepository';
import { useAlert } from '../../components/common/Alerts/AlertContext';

const UploadRequirementsPage = () => {
    const [featureData, setFeatureData] = useState([]);
    const [fileId, setFileId] = useState();
    const { showAlert } = useAlert();
   
    /**
     *  When a file is uploaded to table, set featureData to contain fileContents
     *  this will render a cardGrid of requirements card
     */
    const handleFileUpload = async (file, fileMetadata) => {
        try {
            const fileContents = await FileReaderUtility.readAsText(file);
            const jsonFileContents = JSON.parse(fileContents);
            setFeatureData([...jsonFileContents]);
            await setFileId(fileMetadata.id);
        } catch (error) {
            console.error('Error rendering the uploaded file', error);
            showAlert("error", "Error rendering the uploaded file");
        }
    }

    /**
     * When a file is selected from the table, sets featureData to contain fileContents
     * this will render a cardGrid of user story card
     */
    const handleFileSelection = async (fileContents, fileMetadata) => {
        try {
            const jsonFileContents = JSON.parse(fileContents);
            setFeatureData([...jsonFileContents]);
            await setFileId(fileMetadata.id);
        } catch (error) {
            console.error('Error processing the selected file', error);
            showAlert("error", "Error processing the selected file");
        }
    }
    /**
     * When a user story card is edited and saved this function is invoked
     * @param {*} fileId 
     * @param {*} recordId 
     * @param {*} editedData 
     */
    const handleRequirementsEdit = async (fileId, recordId, editedData) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.updateRecordInFile(fileId = fileId, recordId = recordId, editedData = editedData)
            if (result.success) {
                showAlert("success", "User story updated");
            }
        }
        catch (error) {
            console.error("Error encountered while trying to edit user story:", error);
            showAlert("error", "Failed to update user story please try again");
        }
    };
    /**
     * When a user story card is created and saved this function is invoked
     * @param {} fileId 
     * @param {*} newData 
     */
    const handleRequirementsAdd = async (fileId, newData) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.addRecordToFile(fileId = fileId, newData = newData);
            if (result.success) {
                showAlert("success", "User story added");
            }
        }
        catch (error) {
            console.error("Error encountered while trying to add user story:", error);
            showAlert("error", "Failed to add user story please try again");
        }
    }

    const handleRequirementsDelete = async (fileId, recordId) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.deleteRecordInFile(fileId=fileId,recordId=recordId);
            console.log(result)
            if (result.success) {
                showAlert("success", "User story deleted");
            }
        }
        catch (error) {
            console.error("Error encountered while trying to delete user story", error)
            showAlert("error", "Failed to delete user story please try again");
        }
    }

    return (
        <UserStoryContextProvider
            handleFileUpload={handleFileUpload}
            handleFileSelection={handleFileSelection}
            handleRequirementsEdit={handleRequirementsEdit}
            handleRequirementsAdd={handleRequirementsAdd}
            handleRequirementsDelete={handleRequirementsDelete}>
            <Container> {/* Set maxWidth to false */}
                <Typography variant='h3'>User Story Uploader</Typography>
                <hr></hr>
                <Grid container spacing={0}> {/* Remove spacing */}
                    <Grid item xs={6} style={{ display: 'flex' }}> {/* Use half of the width */}
                        <UserStoryManagementModal style={{ flexGrow: 1 }} /> {/* Allow it to grow */}
                    </Grid>
                    <Grid item xs={6} style={{ display: 'flex', justifyContent: 'flex-end' }}> {/* Align to the end */}
                        <UserStoryTable style={{ flexGrow: 1 }} /> {/* Allow it to grow */}
                    </Grid>
                </Grid>
                <Box mt={4}>
                    <FeatureVisualizer featureData={featureData} fileId={fileId}/>
                </Box>
            </Container>
        </UserStoryContextProvider>
    )
}

export default UploadRequirementsPage