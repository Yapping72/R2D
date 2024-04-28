import React from 'react';
import { Box, ButtonGroup, Button, Tooltip } from '@mui/material/';
import { CheckCircleOutline, DeleteOutline, CancelOutlined } from '@mui/icons-material';
import SearchIcon from '@mui/icons-material/Search';

const JobButtons = ({ jobStatus }) => {
    // Define the allowed job statuses for each button
    // Draft (Invincible to users) --> Queued --> 
    const submitAllowedStatuses = ["Draft", "Queued", "Error Failed to Submit", "Completed"];
    const abortAllowedStatuses = ["Processing"];
    const deleteAllowedStatuses = ["Draft", "Queued", "Error Failed to Submit", "Completed", "Error Failed to Process"];

    // Check if submit button should be disabled
    const isSubmitDisabled = !submitAllowedStatuses.includes(jobStatus);
    // Check if cancel button should be disabled
    const isAbortDisabled = !abortAllowedStatuses.includes(jobStatus);
    // Check if delete button should be disabled
    const isDeleteDisabled = !deleteAllowedStatuses.includes(jobStatus);

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
                    <Button variant='outlined'><SearchIcon /></Button>
                </Tooltip>
                {/* Submit button with tooltip */}
                <Tooltip title="Submit or Resubmit Job for Processing">
                    <Button variant='outlined' color="success" disabled={isSubmitDisabled}><CheckCircleOutline/></Button>
                </Tooltip>
                {/* Delete button with tooltip */}
                <Tooltip title="Delete job">
                    <Button variant='outlined' color="error" disabled={isDeleteDisabled}><DeleteOutline/></Button>
                </Tooltip>
                {/* Cancel button with tooltip */}
                <Tooltip title="Abort job processing">
                    <Button variant='outlined' color='secondary' disabled={isAbortDisabled}><CancelOutlined/></Button>
                </Tooltip>
            </ButtonGroup>
        </Box>
    );
}

export default JobButtons;
