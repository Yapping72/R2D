import React, { useState } from 'react'
import {Button, Container, Divider} from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import UserStoryAccordion from './UserStoryAccordion';
import UserStoryTableModal from './UserStoryTableModal';
import UserStoryJobHandler from '../../../utils/JobHandling/UserStoryJobHandler';
import R2DConfirmationDialog from '../Dialog/R2DConfirmationDialog';
import InformationPaperCard from '../Cards/InformationPaperCard';

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

const FeatureVisualizer = ({ filesData, handleRemoveSelectedFile, handleUserStorySubmit}) => {

    const handleSubmitUserStoryForProcessing = async () => {
        // Validate and sanitize 
        // Merge and extract contents as Job Parameters
        const userStoryJobHandler = new UserStoryJobHandler(filesData);
        userStoryJobHandler.populateJobParameters(filesData);
        const result = await userStoryJobHandler.addJobToQueue();
        handleUserStorySubmit(result); // Pass result back to caller
        setOpenConfirmDialog(false);
    }

    // Display confirmation dialog prompting users if they want to add job to queue
    const [openConfirmDialog, setOpenConfirmDialog] = useState(false);
    const handleOpenConfirmDialog = () => {
        setOpenConfirmDialog(true);
    };

    const handleCloseConfirmDialog = () => {
        setOpenConfirmDialog(false);
    };


    // Remove the selected file from filesData 
    const handleRemove = (index) => {
        handleRemoveSelectedFile(index);
    };

    return (
        <Container>
            <InformationPaperCard
                title="Select User Stories For Analysis" 
                description=" You may select one or more uploaded files containing user stories for analysis.
                User stories queued for analysis should be descriptive and comprehensive to ensure the proposed design meets your requirements."
            >
            <UserStoryTableModal></UserStoryTableModal>
            </InformationPaperCard>
            {filesData.map((fileData, index) => (
                <React.Fragment key={uuidv4()}>
                    <UserStoryAccordion fileData={fileData} index={index} handleRemove={handleRemove} />
                    <Divider sx={{ my: 1 }}></Divider>
                </React.Fragment>
            ))}
            {filesData.length > 0 && (
                <Button variant="outlined" onClick={handleOpenConfirmDialog}>
                    Submit for Processing
                </Button>
            )}
            <R2DConfirmationDialog
                open={openConfirmDialog}
                title="Confirm Submission"  
                content="The user stories you have selected are ready to be added to your job queue. You will have the opportunity to review and submit them for processing on the next page."
                onConfirm={handleSubmitUserStoryForProcessing}
                onCancel={handleCloseConfirmDialog}
            />
        </Container>
    );
};

export default FeatureVisualizer;