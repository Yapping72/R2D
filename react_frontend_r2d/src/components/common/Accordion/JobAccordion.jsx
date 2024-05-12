import React, { useState } from 'react';
import { Box, Tooltip, IconButton, Accordion, AccordionSummary, AccordionDetails, Typography, Stack, Divider } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { renderStatus } from '../Tables/GenericJobTable';
import DownloadIcon from '@mui/icons-material/Download';
import FileDownloadUtility from '../../../utils/FileHandling/FileDownloaderUtility';
import UserStoryJobHandler from '../../../utils/JobHandling/UserStoryJobHandler';
import { useAlert } from '../Alerts/AlertContext';

/**
 * Base JobAccordion component, 
 * @param {object} jobParameters - Dictionary object that contains job_id, tokens, job_status and parameters.job_parameters as keys.
 * @param {Component} children - Component that renders job parameters (jobParameters.parameters.job_parameters) 
 * @returns Accordion that displays job_id, token_count and job_status as accordion summary, on expand, displays children
 */

const JobAccordion = ({ jobParameters = null, children = null, defaultExpanded = true }) => {
    const [expanded, setExpanded] = useState(defaultExpanded);
    const { showAlert } = useAlert();

    const handleExpansion = () => {
        setExpanded(!expanded);
    };

    const handleDownload = async () => {
        const handler = new UserStoryJobHandler();
        try {
            console.log(jobParameters.job_id);
            let result = await handler.retrieveJobFromQueue(jobParameters.job_id);
            const fileName = `${jobParameters.job_id}_${jobParameters.job_status}.json`
            FileDownloadUtility.downloadJson(result.data, fileName);
        }
        catch (error) {
            console.error("Failed to download job parameters", error);
            showAlert('error',"Failed to download job parameters.")
        }
    }
    return (
        <Accordion
            onChange={handleExpansion}
            expanded={expanded}
        >
            <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel-content"
                id="panel-header"
            >
                <Stack
                    direction="row"
                    divider={<Divider orientation="vertical" flexItem />}
                    spacing={2}
                >
                    <Typography>{jobParameters.job_id}</Typography>
                    <Typography>{jobParameters.tokens}</Typography>
                    <>{renderStatus(jobParameters.job_status)}</>
                    <Box>
                    <Tooltip title="Download Job Parameters">
                    <IconButton 
                        color="primary"
                        size='small'
                        onClick={handleDownload}><DownloadIcon></DownloadIcon></IconButton>
                    </Tooltip>
                    </Box>
                </Stack>
            </AccordionSummary>
            <AccordionDetails>
                {/*Pass in jobParameters.parameter to children component, children component renders*/}
                {children}
            </AccordionDetails>
        </Accordion>
    );
};

export default JobAccordion;
