import React from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, Grid, IconButton, Badge, Chip, Tooltip } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DeleteIcon from '@mui/icons-material/Delete';
import UserStoryCardGrid from '../Cards/UserStoryCardGrid';
/**
 * Displays an accordion for each file, showing file metadata and a grid of user stories.
 * Each file can be expanded to reveal detailed information including features and sub-features associated with the file.
 * 
 * @param {Object} fileData - Contains the metadata and feature data for a single file.
 *                            * fileData should contain the fileMetadata (features and sub_features)
 * @param {number} index - The index of the file in the list, used for handling deletions.
 * @param {Function} handleRemove - A function to remove the file from the list, triggered by the delete icon.
 * @returns {JSX.Element} An MUI Accordion component that wraps detailed information about a file.
 */

const UserStoryAccordion = ({ fileData, index, handleRemove }) => {
    return (
        <Accordion
            defaultExpanded={true}
        >
            <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="user-story-card-grid-content"
                id="user-story-card-grid-header"
            >
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={11}>
                        <Grid container direction="column">
                            <Grid item>
                                <Typography variant="h6">
                                    {fileData.fileMetadata.filename}
                                </Typography>
                            </Grid>
                            <Tooltip title="Features" placement="left-start" arrow>
                                <Grid item>
                                    {Array.from(fileData.fileMetadata.features).map((feature, index) => (
                                        <Chip
                                            key={`${feature}-${index}`} 
                                            label={feature} 
                                            size="small" 
                                            style={{ marginRight: '5px' }}
                                            variant="outlined" 
                                            color="primary"
                                        />
                                    ))}
                                </Grid>
                            </Tooltip>
                            <Tooltip title="Sub Features" placement="left-end" arrow>
                                <Grid item>
                                    {Array.from(fileData.fileMetadata['sub features']).map((sub_feature, index) => (
                                        <Chip
                                            key={`${sub_feature}-${index}`} 
                                            label={sub_feature} 
                                            size="small" 
                                            style={{ marginRight: '5px' }}
                                            variant="outlined" 
                                            color="secondary"
                                        />
                                    ))}
                                </Grid>
                            </Tooltip>
                        </Grid>
                    </Grid>
                    <Grid item xs={12} sm={1} sx={{ textAlign: 'right' }}>
                        <Tooltip title="File Id" arrow>
                            <Badge
                                badgeContent={fileData.fileMetadata.id}
                                color='success'
                                variant='outlined'
                                sx={{ mr: 2 }} // Adds right margin
                            />
                        </Tooltip>
                        <Tooltip title="Exclude from analysis"> 
                            <IconButton onClick={() => { handleRemove(index) }}> {/*Removes the user stories from feature visualizer*/}
                                <DeleteIcon />
                            </IconButton>
                        </Tooltip>
                    </Grid>
                </Grid>
            </AccordionSummary>
            <AccordionDetails>
                <UserStoryCardGrid featureData={fileData.featureData} fileId={fileData.fileId} />
            </AccordionDetails>
        </Accordion>
    );
};

export default UserStoryAccordion;