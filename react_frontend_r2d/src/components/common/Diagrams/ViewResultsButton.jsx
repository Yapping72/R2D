import React, { useState } from 'react';
import { Box, ButtonGroup, Button, Tooltip } from '@mui/material/';

const ViewResultsButton = ({jobId, onViewResults }) => {
    
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', '& > *': { m: 1 } }}>
            <ButtonGroup aria-label="Basic button group">
                <Tooltip title="View the generated user stories or diagrams">
                    <span>
                        <Button
                            variant="outlined"
                            onClick={() => onViewResults(jobId)} // Call onViewResults with jobId
                        >
                            Results
                        </Button>
                    </span>
                </Tooltip>
            </ButtonGroup>
        </Box>
    );
};

export default ViewResultsButton;