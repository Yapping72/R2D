import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

const InformationPaperCard = ({ title, description, children }) => {
    return (
        <Paper sx={{ p: 2, mb: 2, background: 'black', border: '1px solid', borderColor: 'white' }}>
            <Typography variant="h5" gutterBottom>
                {title}
            </Typography>
            <Typography>
                {description}
            </Typography>
            <Box sx={{ mt: 2 }}>
                {children}
            </Box>
        </Paper>
    );
};

export default InformationPaperCard;
