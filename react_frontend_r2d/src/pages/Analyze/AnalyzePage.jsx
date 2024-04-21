import React from 'react'
import {Container, Box, Typography} from '@mui/material'

import { UserStoryContextProvider } from '../../components/common/UserStory/UserStoryContextProvider';
import UserStoryTable from '../../components/common/UserStory/UserStoryTable'
import { useAlert } from '../../components/common/Alerts/AlertContext';
import { Toys } from '@mui/icons-material';


const AnalyzePage = () => {
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

    return(
        <UserStoryContextProvider handleFileSelection={handleFileSelection}>
        <Container>
        <Box>
            <Typography variant='h4'> Queue Jobs for Analysis </Typography>
            <h3> Add Tab here that switches between queue and results </h3>
            <Typography>Job Queue Table: 
            status: SENDING, SENT, PROCESSING, SUCCESS, ERROR</Typography>
            row actions: START JOB, CANCEL JOB, DOWNLOAD JOB PARAMETERS, VIEW JOB PARAMETERS
            table actions: ADD JOB TO QUEUE
            <h3>Second tab could be a mermaid renderer</h3>

        </Box>
        
        </Container>
        </UserStoryContextProvider>
    )
}
export default AnalyzePage