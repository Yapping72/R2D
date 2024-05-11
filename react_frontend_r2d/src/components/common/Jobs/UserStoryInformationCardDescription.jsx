import React from 'react';
import { Box, Typography, Chip, Stack } from '@mui/material'
import { renderStatus } from '../Tables/GenericJobTable';


// Actions mapped to statuses that permit them
const actionsMapping = {
    'Jobs that can be submitted:': ['Draft', 'Queued', 'Error Failed to Submit', 'Completed', 'Job Aborted'],
    'Jobs that can be deleted:': ['Draft', 'Queued', 'Error Failed to Submit', 'Error Failed to Process', 'Completed', 'Job Aborted'],
    'Jobs that can be aborted:': ['Processing']
};

const UserStoryInformationCardDescription = () => {
    return (
        <Box>
            <Typography variant='subtitle1'  sx={{ mb: 1 }}>
                <strong>Important:</strong> Only jobs with a {renderStatus('Completed')} status are persisted on our backend servers. All other statuses are maintained locally and will be automatically deleted after 7 days or when the browser cache is cleared.
                Below is a list of supported actions for each job status.
            </Typography>
            <Stack spacing={2}>
                {Object.entries(actionsMapping).map(([action, statuses]) => (
                    <Box key={action}>
                        <Typography variant="subtitle1">{action}</Typography>
                        <Stack direction="row" spacing={1} wrap="wrap">
                            {statuses.map(status => (
                                <Box key={status} sx={{ display: 'flex', alignItems: 'center', margin: 1 }}>
                                    {renderStatus(status)}
                                </Box>
                            ))}
                        </Stack>
                    </Box>
                ))}
            </Stack>
        </Box>
    );
};

export default UserStoryInformationCardDescription;