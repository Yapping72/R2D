import React from 'react';
import { Paper, Typography, Box } from '@mui/material';


/**
 * Renders title, description and child components within a paper that contains white borders
 * @param {title} title h5 typography element 
 * @param {description} description should be a Typography element smaller than h5
 * @param {children} children can be buttons, buttonGroups or any logical component to provide functionality to the InformationCard 
 * @returns 
 */
const InformationPaperCard = ({ title, description, children }) => {
    return (
        <Paper sx={{ p: 2, mb: 2, background: 'black', border: '1px solid', borderColor: 'white', overflow:'auto' }}>
            <Typography variant="h5" gutterBottom>
                {title}
            </Typography>
            {description}
            <Box sx={{ mt: 2 }}>
                {children}
            </Box>
        </Paper>
    );
};

export default InformationPaperCard;
