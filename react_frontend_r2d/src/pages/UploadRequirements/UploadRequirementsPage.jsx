import { useState } from 'react';
import { AlertProvider } from '../../components/common/Alerts/AlertContext';
import {Box, Typography, Container, Grid} from "@mui/material";
import UserStoryManagementModal from '../../components/common/UserStory/UserStoryManagementModal';
import UserStoryTable from '../../components/common/UserStory/UserStoryTable';
import FeatureVisualizer from '../../components/common/UserStory/FeatureVisualizer';
import { UserStoryContextProvider } from '../../components/common/UserStory/UserStoryContextProvider';
import FileReaderUtility from '../../utils/FileHandling/FileReaderUtility';
import { UserStoryFileRepository } from '../../utils/Repository/UserStoryFileRepository';

const UploadRequirementsPage = () => {  
    const [featureData, setFeatureData] = useState([]);
    const [fileTitle, setFileTitle] = useState();
    const [fileId, setFileId] = useState();

    /**
     *  When a file is uploaded to table, set featureData to contain fileContents
     *  this will render a cardGrid of requirements card
     */
    const handleFileUpload = async (file, fileMetadata) => {
        try {
            const fileContents = await FileReaderUtility.readAsText(file);  
            const jsonFileContents = JSON.parse(fileContents);
            setFeatureData(jsonFileContents);
            await setFileTitle(fileMetadata.filename);
            await setFileId(fileMetadata.id); 
        } catch (error) {
            console.error('Error processing the selected file', error);
        }
    }   

    /**
     * When a file is selected from the table, sets featureData to contain fileContents
     * this will render a cardGrid of requirements card
     */
    const handleFileSelection = async (fileContents, fileMetadata) => {
        try {
            const jsonFileContents = JSON.parse(fileContents);
            setFeatureData(jsonFileContents);
            await setFileTitle(fileMetadata.filename);
            await setFileId(fileMetadata.id);
        } catch (error) {
            console.error('Error processing the selected file', error);
        }
    }

    const handleRequirementsEdit = async (fileId, recordId, editedData) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.updateRecordInFile(fileId=fileId, recordId=recordId, editedData=editedData)
            console.log(result)
        } 
        catch (error) {
            console.error("Error encountered while trying to save changes to requirements:", error);
        }
    };

    const handleRequirementsAdd = async (fileId, newData) => {
        try {
            const repository = new UserStoryFileRepository();
            let result = await repository.addRecordToFile(fileId=fileId, newData=newData);
            console.log(result)
        } 
        catch (error) {
            console.error("Error encountered while trying to save changes to requirements:", error);
        }
    }

    return (
        <UserStoryContextProvider 
        handleFileUpload={handleFileUpload} 
        handleFileSelection={handleFileSelection} 
        handleRequirementsEdit={handleRequirementsEdit}
        handleRequirementsAdd={handleRequirementsAdd}>
        <AlertProvider>
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
                    <FeatureVisualizer featureData={featureData} fileId={fileId} fileName={fileTitle} />
                </Box>
            </Container>
        </AlertProvider>
    </UserStoryContextProvider>
    )
}

export default UploadRequirementsPage