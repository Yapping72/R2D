import React, { useState } from 'react';
import { Box, ButtonGroup, Button, Tooltip } from '@mui/material/';
import { DeleteOutline, CancelOutlined, ArrowUpwardOutlined } from '@mui/icons-material';
import SearchIcon from '@mui/icons-material/Search';
import { useUserStoryJobContext } from './UserStoryJobContextProvider';
import R2DConfirmationDialog from '../Dialog/R2DConfirmationDialog';
import { JobStatus } from '../../../utils/JobHandling/GenericJobHandler';
/**
 * UserStoryJobTable Button Groups
 */
const UserStoryJobQueueButtons = ({ jobStatus, jobId }) => {
    // Retrieve the context to use the add, delete and view job parameters functions
    const { handleViewUserStoryJobParameters, handleSubmitUserStoryJob, handleDeleteUserStoryJob, handleAbortUserStoryJob } = useUserStoryJobContext();

    // Define actions allowed for each job status
    const submitAllowedStatuses = [JobStatus.DRAFT, JobStatus.QUEUED, JobStatus.ERROR_FAILED_TO_SUBMIT, JobStatus.COMPLETED, JobStatus.ABORTED];
    const abortAllowedStatuses = [JobStatus.PROCESSING];
    const deleteAllowedStatuses = [JobStatus.DRAFT, JobStatus.QUEUED, JobStatus.ERROR_FAILED_TO_SUBMIT, JobStatus.ERROR_FAILED_TO_PROCESS, JobStatus.COMPLETED, JobStatus.ABORTED];

    // Check if submit button should be disabled
    const isSubmitDisabled = !submitAllowedStatuses.includes(jobStatus);
    // Check if cancel button should be disabled
    const isAbortDisabled = !abortAllowedStatuses.includes(jobStatus);
    // Check if delete button should be disabled
    const isDeleteDisabled = !deleteAllowedStatuses.includes(jobStatus);

    // Display confirmation dialog when user attempts to delete a job from queue
    const [deleteJobConfirmationDialog, setDeleteJobConfirmationDialog] = useState(false);

    // Displays a dialog when users attempts to delete job from queue 
    const handleOpenDeleteJobConfirmationDialog = () => {
        setDeleteJobConfirmationDialog(true);
    };

    // Closes the delete job confirmation dialog
    const handleCloseDeleteJobConfirmationDialog = () => {
        setDeleteJobConfirmationDialog(false);
    };

    // Invoked when user clicks on the view job parameters button
    const viewJobParameters = () => {
        handleViewUserStoryJobParameters(jobId);
    }

    // Invoked when user clicks on the submit button
    const submitJob = () => {
        handleSubmitUserStoryJob(jobId);
    }

    // Invoked when user clicks on the delete button
    const deleteJob = () => {
        handleDeleteUserStoryJob(jobId);
        handleCloseDeleteJobConfirmationDialog();
    }

    const abortJob = () => {
        handleAbortUserStoryJob(jobId);
    }

    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                '& > *': {
                    m: 1,
                },
            }}
        >
            <ButtonGroup aria-label="Basic button group">
                {/* View Job Parameters*/}
                <Tooltip title="View Job Parameters">
                    <span>
                        <Button
                            variant='contained'
                            onClick={viewJobParameters}><SearchIcon /></Button>
                    </span>
                </Tooltip>
                {/* Submit button with tooltip */}
                <Tooltip title="Submit or Resubmit Job for Processing">
                    <span>
                        <Button
                            variant='contained'
                            color="success"
                            disabled={isSubmitDisabled}
                            onClick={submitJob}
                        ><ArrowUpwardOutlined /></Button>
                    </span>
                </Tooltip>
                {/* Delete button with tooltip */}
                <Tooltip title="Delete job">
                    <span>
                        <Button
                            variant='contained'
                            color="error"
                            disabled={isDeleteDisabled}
                            onClick={handleOpenDeleteJobConfirmationDialog}><DeleteOutline /></Button>
                    </span>
                </Tooltip>
                {/* Cancel button with tooltip */}
                <Tooltip title="Abort job processing">
                    <span>
                        <Button 
                            variant='contained' 
                            color='secondary'
                            disabled={isAbortDisabled}
                            onClick={abortJob}><CancelOutlined /></Button>
                    </span>
                </Tooltip>
            </ButtonGroup>
            <R2DConfirmationDialog
                open={deleteJobConfirmationDialog}
                title="Confirm Job Deletion"
                content="Are you sure you want to delete this job? Deleting a job will permanently remove it from the system. Note: Only jobs in 'Draft', 'Queued', 'Error' or 'Completed' states can be deleted."
                onCancel={handleCloseDeleteJobConfirmationDialog}
                onConfirm={deleteJob}
            />
        </Box>
    );
}

export default UserStoryJobQueueButtons;
