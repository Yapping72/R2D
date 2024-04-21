import React from 'react'
import { Typography, Button, Container, Divider, Box, Paper } from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import UserStoryAccordion from './UserStoryAccordion';
import UserStoryTableModal from './UserStoryTableModal';
import UserStoryJobHandler from '../../../utils/JobHandling/UserStoryJobHandler';

/**
 * `FeatureVisualizer` renders a list of `UserStoryCardGrid` components, each corresponding to a set of user stories or requirements.
 * Each `UserStoryCardGrid` is associated with a specific file's data and is displayed under a heading that shows the file's identifier.
 * This component allows for viewing multiple sets of data, each associated with different files.
 * 
 * Props:
 * - `filesData` (Array): An array of objects, where each object contains:
 *    - `fileId` (string): Identifier for the file associated with the requirements, used for edit operations.
 *    - `featureData` (Array): Data for the features associated with the file. This data is displayed in the `UserStoryCardGrid`.
 *      Each object in this array should include details such as `feature`, `sub_feature`, `id`, `requirement`, and optionally `services_to_use`.
 * 
 * @param {Object} props - The props object for the component.
 * @param {Array} props.filesData - The array of data for multiple files, each including feature data and a fileId.
 * 
 * @returns {ReactElement} The `FeatureVisualizer` component that renders multiple `UserStoryCardGrid` components, each under a file identifier heading.
 */

const FeatureVisualizer = ({ filesData, handleRemoveSelectedFile}) => {

    const handleSubmitUserStoryForProcessing = () => {
        // Validate and sanitize 
        // Merge and extract contents as Job Parameters
        // Send to Job Queue
        const userStoryJobHandler = new UserStoryJobHandler(filesData);
        userStoryJobHandler.populateJobParameters(filesData);
        console.log(filesData)
    }

    // Remove the selected file from filesData 
    const handleRemove = (index) => {
        handleRemoveSelectedFile(index);
    };
    
    return (
        <Container>
            <Paper 
                sx={{ p: 2, mb: 2, background:'black', border:'1px solid', borderColor:'white'}
            }>
                <Typography variant="h5" gutterBottom>
                    Select User Stories For Analysis
                </Typography>
                <Typography>
                    You may select one or more uploaded files containing user stories for analysis.
                    User stories queued for analysis should be descriptive and comprehensive to ensure the proposed design meets your requirements.
                </Typography>
                <Box sx={{ mt: 2 }}>
                    <UserStoryTableModal />
                </Box>
            </Paper>
            {filesData.map((fileData, index) => (
                <React.Fragment key={uuidv4()}>
                    <UserStoryAccordion fileData={fileData} index={index} handleRemove={handleRemove} />
                    <Divider sx={{my:1}}></Divider>
                </React.Fragment>
            ))}
            {filesData.length > 0 && (
                <Button variant="outlined" onClick={handleSubmitUserStoryForProcessing}>
                    Submit for Processing
                </Button>
            )}
        </Container>
    );
};

export default FeatureVisualizer;