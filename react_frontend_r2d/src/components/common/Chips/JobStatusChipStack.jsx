import React, { useEffect, useState } from 'react';
import { Chip, Stack, Tooltip } from '@mui/material';
import { useAlert } from '../Alerts/AlertContext';

/**
 * Counts the number of jobs that are in a particular status. 
 * @param {object} repository - Concrete JobQueue repository that implements a handleReadAll function
 * @returns Horizontally stacked chips. Each chip corresponds to particular job status. Each chip will denote the number of jobs in a particular status.
 */
const JobStatusChipStack = ({repository}) => {
    const [jobStatusCounts, setJobStatusCounts] = useState({});
    const { showAlert } = useAlert();
    
    useEffect(() => {
        const fetchData = async () => {
            const response = await repository.handleReadAll();
            if (response.success) {
                console.debug(response.data)
                updateJobStatusCounts(response.data);
            } else {
                showAlert('error', `We're having trouble retrieving uploaded files at the moment. Please try again shortly, or reach out to our support team for assistance. We appreciate your patience.`)
            }
        };
        fetchData();
    }, [repository]);

    const updateJobStatusCounts = (data) => {
        const counts = data.reduce((acc, record) => {
            const status = record.job_status;  // Assuming the status is stored in job_status
            if (status) {
                acc[status] = (acc[status] || 0) + 1;
            }
            return acc;
        }, {});

        setJobStatusCounts(counts);
        console.debug("Updated job status counts:", counts);
    };

    
    const renderStatusChip = (status, count) => {
        switch (status) {
            case "Draft":
                return (
                    <Tooltip title="Total number of jobs in draft status that can be submitted.">
                        <Chip label={`${status} (${count})`} variant='outlined' />
                    </Tooltip>
                );
            case "Queued":
                return (
                    <Tooltip title="Total number of jobs in queued status and ready for submission.">
                        <Chip label={`${status} (${count})`} />
                    </Tooltip>
                );
            case "Submitted":
                return (
                    <Tooltip title="Total number of jobs in submitted status and pending LLM analysis.">
                        <Chip label={`${status} (${count})`} color='primary' variant='outlined' />
                    </Tooltip>
                );
            case "Error Failed to Submit":
                return (
                    <Tooltip title="Total number of jobs in submission error status.">
                        <Chip label={`Submission Error (${count})`} color='error' />
                    </Tooltip>
                );
            case "Error Failed to Process":
                return (
                    <Tooltip title="Total number of jobs in processing error error status.">
                        <Chip label={`Processing Error (${count})`}color='error' />
                    </Tooltip>
                );
            case "Processing":
                return (
                    <Tooltip title="Total number of jobs currently being processed.">
                        <Chip label={`Processing (${count})`} color='primary' />
                    </Tooltip>
                );
            case "Job Aborted":
                return (
                    <Tooltip title="Total number of jobs that have been aborted.">
                        <Chip label={`${status} (${count})`} color='warning' />
                    </Tooltip>
                );
            case "Completed":
                return (
                    <Tooltip title="Total number of jobs that have been completed.">
                        <Chip label={`Aborted (${count})`} color='success' />
                    </Tooltip>
                );
            default:
                return null;
        }
    };

    return (
        <Stack direction="row" spacing={1} alignItems="center" justifyContent="left">
            {Object.entries(jobStatusCounts).map(([status, count]) => (
                <React.Fragment key={status}>
                    {renderStatusChip(status, count)}
                </React.Fragment>
            ))}
        </Stack>
    );
}

export default JobStatusChipStack;
