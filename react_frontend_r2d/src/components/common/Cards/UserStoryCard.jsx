import React, { useState } from 'react';
import {Card, CardContent, CardActions, Button, Typography, Divider, Pagination, Chip } from '@mui/material';
import EditUserStoryDialog from '../Dialog/EditUserStoryDialog';


/**
 * Displays a card for a user story with functionality to edit and delete the story.
 * @param {string} feature - Name of the feature the user story belongs to.
 * @param {string} subFeature - Name of the sub-feature the user story belongs to.
 * @param {string} requirement - Description of the user story requirement.
 * @param {string} recordId - Unique identifier for the user story.
 * @param {array} servicesToUse - List of services to use in this user story.
 * @param {string} fileId - Identifier for the file associated with the user story. To be refactored to identificationId
 * @param {string} additionalInformation - Additional information about the user story.
 * @param {string} acceptanceCriteria - Acceptance criteria for the user story.
 * @param {function} handleRequirementsEdit - Function to handle editing user story details.
 * @param {function} handleRequirementsDelete - Function to handle deleting the user story.
 * @returns {component} Paginated User story card that displays the information above. 
 */
const UserStoryCard = ({
  feature,
  subFeature,
  id,
  requirement,
  recordId,
  servicesToUse,
  fileId,
  additionalInformation,
  acceptanceCriteria,
  handleRequirementsEdit,
  handleRequirementsDelete,
}) => {
  const [isEditMode, setIsEditMode] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);

  const handleEditClick = () => setIsEditMode(true);
  const handleClose = () => setIsEditMode(false);

  const saveEdits = (editedData) => {
    handleRequirementsEdit(fileId, recordId, editedData);
    setIsEditMode(false);
  };

  const handleDeleteClick = () => handleRequirementsDelete(fileId, recordId);
  const handleChangePage = (event, value) => setCurrentPage(value);

  const pageContent = (page) => {
    switch (page) {
      case 1:
        return (
          <>
            
            <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
              {feature || 'Feature'}
            </Typography>
            <Typography variant="h5" component="div">
              {subFeature || 'Subfeature'}
            </Typography>
            <Typography sx={{ mb: 1.5 }} color="text.secondary">
              {id || 'ID'}
            </Typography>
            <Typography variant="body2">
              {requirement || 'Requirement'}
            </Typography>
            <Divider sx={{ my: 2 }} />
            {servicesToUse && servicesToUse.length > 0 && (
              <Typography variant='body2'>
                <strong>Services to Use:</strong>
              </Typography>
            )}
            <ol style={{ margin: 0 }}>
              {servicesToUse.map((service, index) => (
                <li key={index}>
                  <Typography variant='body2'>{service}</Typography>
                </li>
              ))}
            </ol>
          </>
        );
      case 2:
        return (
          <>
            <Typography variant="body2" component="div">
              <strong>Acceptance Criteria:</strong>
              <br></br>
              {acceptanceCriteria || 'Not specified'}
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Typography variant="body2" component="div">
              <strong>Additional Information:</strong>
              <br></br>
              {additionalInformation || 'Not specified'}
            </Typography>
            <Divider sx={{ my: 2 }} />
          </>
        );
      default:
        return null;
    }
  };

  return (
    <>
      <Card
        variant="outlined"
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'auto',
          transition: 'transform 0.3s ease', // Smooth transition for transform change
          transform: 'scale(1)', // Normal state scale
          ':hover': {
            transform: 'scale(1.025)'  // Scale up by 5% on hover
          }
        }}>
        <CardContent sx={{ flex: '1 0 auto' }}>
          {pageContent(currentPage)}
        </CardContent>
        <CardActions>
          <Button size="small" onClick={handleEditClick}>Edit</Button>
          <Button size="small" onClick={handleDeleteClick}>Delete</Button>
          <Pagination count={2} page={currentPage} onChange={handleChangePage} color="primary" />
        </CardActions>
      </Card>
      <EditUserStoryDialog
        open={isEditMode}
        handleClose={handleClose}
        feature={feature}
        subFeature={subFeature}
        id={id}
        requirement={requirement}
        services_to_use={servicesToUse}
        acceptance_criteria={acceptanceCriteria}
        additional_information={additionalInformation}
        handleSave={saveEdits}
        recordId={recordId}
      />
    </>
  );
};

export default UserStoryCard;
