import React, { useState } from 'react';
import { Box, Divider } from '@mui/material';
import GenericJobTable from '../Tables/GenericJobTable';
import DiagramVisualizer from './DiagramVisualizer';
import ViewResultsButton from './ViewResultsButton';
import { UserStoryJobQueueRepository } from '../../../utils/Repository/UserStoryJobQueueRepository';

const CompletedJobTable = () => {
    const [visualizerOpen, setVisualizerOpen] = useState(false);
    const [selectedJobId, setSelectedJobId] = useState('');

    const handleOpenVisualizer = (jobId) => {
        setSelectedJobId(jobId);
        setVisualizerOpen(true);
    };

    const handleCloseVisualizer = () => {
        setVisualizerOpen(false);
        setSelectedJobId('');
    };

    return (
        <>
            <Box>
                <GenericJobTable
                    repository={new UserStoryJobQueueRepository()}
                    buttonGroup={<ViewResultsButton onViewResults={handleOpenVisualizer} />}
                    showOnlyCompleted={true}
                    renderButtonGroupChild={true}
                />
                <Divider sx={{ my: 1 }} />
            </Box>
            {visualizerOpen && (
                <DiagramVisualizer
                    jobId={selectedJobId}
                    open={visualizerOpen}
                    onClose={handleCloseVisualizer}
                />
            )}
        </>
    );
};

export default CompletedJobTable;
