import { useState } from 'react';
import { AlertProvider } from '../../components/common/Alerts/AlertContext';
import {Box, Typography, Container, Grid} from "@mui/material";
import RequirementsFileManagementModal from '../../components/common/Requirements/RequirementsFileManagementModal';
import RequirementsTable from '../../components/common/Requirements/RequirementsTable';
import FeatureVisualizer from '../../components/common/Requirements/FeatureVisualizer';
import { RequirementsContextProvider } from '../../components/common/Requirements/RequirementsContextProvider';
import FileReaderUtility from '../../utils/FileReaders/FileReaderUtility';
import { RequirementsFileRepository } from '../../utils/Repository/RequirementsFileRepository';

const UploadRequirementsPage = () => {  
    const [featureData, setFeatureData] = useState([]);
    const [fileTitle, setFileTitle] = useState();
    const [fileId, setFileId] = useState();
    const [accordionTitle, setAccordionTitle] = useState("Upload or load requirements to begin");

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
            const title = `Requirements for ${fileTitle}-${fileId}`
            setAccordionTitle(title);
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
            const title = `Requirements for ${fileTitle}-${fileId}`
            setAccordionTitle(title);
        } catch (error) {
            console.error('Error processing the selected file', error);
        }
    }

    const handleRequirementsEdit = async (fileId, recordId, editedData) => {
        try {
            const repository = new RequirementsFileRepository();
            let result = await repository.updateRecordInFile(fileId=fileId, recordId=recordId, editedData=editedData)
            console.log(result)
        } 
        catch (error) {
            console.error("Error encountered while trying to save changes to requirements:", error);
        }
    };

    const handleRequirementsAdd = async (fileId, newData) => {
        try {
            const repository = new RequirementsFileRepository();
            let result = await repository.addRecordToFile(fileId=fileId, newData=newData);
            console.log(result)
        } 
        catch (error) {
            console.error("Error encountered while trying to save changes to requirements:", error);
        }
    }

    return (
        <RequirementsContextProvider 
        handleFileUpload={handleFileUpload} 
        handleFileSelection={handleFileSelection} 
        handleRequirementsEdit={handleRequirementsEdit}
        handleRequirementsAdd={handleRequirementsAdd}>
        <AlertProvider>
            <Container> {/* Set maxWidth to false */}
                 <Box>
                    <Typography variant='h3'>Requirements Uploader</Typography>
                    <hr></hr>
                </Box>
                <Grid container spacing={0}> {/* Remove spacing */}
                    <Grid item xs={6} style={{ display: 'flex' }}> {/* Use half of the width */}
                        <RequirementsFileManagementModal style={{ flexGrow: 1 }} /> {/* Allow it to grow */}
                    </Grid>
                    <Grid item xs={6} style={{ display: 'flex', justifyContent: 'flex-end' }}> {/* Align to the end */}
                        <RequirementsTable style={{ flexGrow: 1 }} /> {/* Allow it to grow */}
                    </Grid>
                </Grid>
                <Box mt={4}>
                    <FeatureVisualizer title={accordionTitle} featureData={featureData} fileId={fileId} fileName={fileTitle} />
                </Box>
            </Container>
        </AlertProvider>
    </RequirementsContextProvider>
    )
}

export default UploadRequirementsPage