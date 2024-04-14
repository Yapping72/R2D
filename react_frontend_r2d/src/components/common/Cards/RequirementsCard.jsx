import {React, useState} from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

import EditRequirementCardDialog from '../Dialog/EditRequirementCardDialog';

const RequirementsCard = ({ 
  feature, 
  subFeature, 
  id, 
  requirement, 
  recordId,
  services_to_use, 
  fileId,
  handleRequirementsEdit,
}) => {
  const [isEditMode, setIsEditMode] = useState(false); // When set to true, dialog appears allowing modification of fields
  const [currentFeature, setCurrentFeature] = useState(feature);
  const [currentSubFeature, setCurrentSubFeature] = useState(subFeature);
  const [currentId, setCurrentId] = useState(id);
  const [currentRequirement, setCurrentRequirement] = useState(requirement);
  const [currentServicesToUse, setCurrentServicesToUse] = useState(services_to_use);

  const handleEditClick = () => {
    setIsEditMode(true);
  };

  const handleClose = () => {
    setIsEditMode(false);
  };

  // Invoke repository to update file
  const saveEditsToDb = (fileId, recordId, editedData) => {
      handleRequirementsEdit(fileId, recordId, editedData);
  }

  // Current implementation of handleSave only displays the changes on the RequirementsCard
  const handleSave = (editedData) => {
    setCurrentFeature(editedData.feature);
    setCurrentSubFeature(editedData.subFeature);
    setCurrentId(editedData.id);
    setCurrentRequirement(editedData.requirement);
    setCurrentServicesToUse(editedData.services_to_use);
    handleClose();
    saveEditsToDb(fileId,recordId,editedData) // commit changes 
  };
 return (
    <>
      <Card variant="outlined" sx={{ height: '100%', display: 'flex', flexDirection: 'column', overflow:'auto'}}>
        <CardContent sx={{ flex: '1 0 auto' }}>
          <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
            {currentFeature || 'Feature'}
          </Typography>
          <Typography variant="h5" component="div">
            {currentSubFeature || 'Subfeature'}
          </Typography>
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            {currentId || 'id'}
          </Typography>
          <Typography variant="body2">
            {currentRequirement || 'Requirement'}
          </Typography>
          {currentServicesToUse && currentServicesToUse.length > 0 && (
            <Typography variant="body2"component="div">
              <hr></hr>
              <strong>Services to Use:</strong>
              <ol style={{ margin: 0 }}>
               {currentServicesToUse.map((service, index) => (
                <li key={service}>{service}</li>
              ))}
              </ol>
            </Typography>
          )}
        </CardContent>
        <CardActions>
          <Button size="small" onClick={handleEditClick}>Edit</Button>
        </CardActions>
      </Card>
      <EditRequirementCardDialog
        open={isEditMode}
        handleClose={handleClose}
        feature={currentFeature}
        subFeature={currentSubFeature}
        id={currentId}
        requirement={currentRequirement}
        services_to_use={currentServicesToUse}
        handleSave={handleSave}
        recordId={recordId}
      />
    </>
  );
};

export default RequirementsCard;
