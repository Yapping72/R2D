import React, { useState } from 'react';
import { Card, CardContent, CardActions, Button, Typography, Divider, Pagination } from '@mui/material';
import EditUserStoryDialog from '../Dialog/EditUserStoryDialog';

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
  const saveEditsToDb = (editedData) => {
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
            {servicesToUse && servicesToUse.length > 0 && (
              <Typography variant='body2'>
                <Divider sx={{ my: 2 }} />
                <strong>Services to Use:</strong>
                <ol style={{ margin: 0 }}>
                  {servicesToUse.map((service, index) => (
                    <li key={index}>{service}</li>
                  ))}
                </ol>
              </Typography>
            )}
          </>
        );
      case 2:
        return (
          <>
            <Typography variant="body2" component="div">
              <strong>Acceptance Criteria:</strong>
              <br></br>
              {acceptanceCriteria || 'Not specified'}
              <Divider sx={{ my: 2 }} />
            </Typography>
            <Typography variant="body2" component="div">
              <strong>Additional Information:</strong>
              <br></br>
              {additionalInformation || 'Not specified'}
              <Divider sx={{ my: 2 }} />
            </Typography>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <>
      <Card variant="outlined" 
      sx={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'auto' }}>
        <CardContent sx={{ flex: '1 0 auto'}}>
          {pageContent(currentPage)}
        </CardContent>
        <CardActions>
          <Button size="small" onClick={handleEditClick}>Edit</Button>
          <Button size="small" onClick={handleDeleteClick}>Delete</Button>
          <Pagination count={2} page={currentPage} onChange={handleChangePage } color="primary" />
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
        handleSave={saveEditsToDb}
        recordId={recordId}
      />
    </>
  );
};

export default UserStoryCard;
