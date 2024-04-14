import React, { useState } from 'react';
import { Card, IconButton } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import './AddRequirementsCard.css'

import { v4 as uuidv4 } from 'uuid';
import EditRequirementCardDialog from '../Dialog/EditRequirementCardDialog';

const AddRequirementCard = ({
  fileId,
  handleRequirementsAdd }) => {
  const [isEditMode, setIsEditMode] = useState(false); // When set to true, dialog appears allowing modification of fields
  const [feature, setFeature] = useState("");
  const [subFeature , setSubFeature] = useState("");
  const [id, setId] = useState("");
  const [requirement, setRequirement] = useState("");
  const [servicesToUse, setServicesToUse] = useState("");
  const [recordId, setRecordId] = useState(uuidv4()); // Creates a record identifier
  
  // Opens the edit card dialog
  const handleClickOpen = () => {
    setIsEditMode(true);
  };

  // Closes the edit card dialog
  const handleCloseDialog = () => {
    setIsEditMode(false);
  }
  const saveCardToDb = (fileId, recordId, newData) => {
    handleRequirementsAdd(fileId, recordId, newData);
  }

  // Displays a new Card
  const handleSave = (newData) => {
    setFeature(newData.feature);
    setSubFeature(newData.subFeature);
    setId(newData.id);
    setRequirement(newData.requirement);
    setServicesToUse(newData.services_to_use);
    handleCloseDialog();
    saveCardToDb(fileId,newData) 
  };

  return (
    <>
      <Card className="add-requirement-card" onClick={handleClickOpen}>
        <IconButton size="large">
          <AddIcon fontSize="inherit" />
        </IconButton>
      </Card>
      <EditRequirementCardDialog
        open={isEditMode}
        handleClose={handleCloseDialog}
        feature={feature}
        subFeature={subFeature}
        id={id}
        requirement={requirement}
        services_to_use={servicesToUse}
        handleSave={handleSave}
        recordId={recordId}
      />
    </>
  );
};

export default AddRequirementCard;
