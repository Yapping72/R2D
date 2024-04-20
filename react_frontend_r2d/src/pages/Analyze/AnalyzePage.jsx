import React from 'react'
import {Container, Box, Typography} from '@mui/material'

import { UserStoryContextProvider } from '../../components/common/UserStory/UserStoryContextProvider';
import UserStoryTable from '../../components/common/UserStory/UserStoryTable'
import { useAlert } from '../../components/common/Alerts/AlertContext';


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
            <hr></hr>
        </Box>
        <UserStoryTable></UserStoryTable>
        </Container>
        </UserStoryContextProvider>
    )
}
export default AnalyzePage