import React, { useState } from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';
import {Typography} from '@mui/material';

/**
 * Dialog that enables editing of requirement cards used on Upload page
 */
const EditRequirementCardDialog = ({ open, handleClose, feature, subFeature, id, requirement, services_to_use, handleSave, recordId }) => {
  const [editedFeature, setEditedFeature] = useState(feature);
  const [editedSubFeature, setEditedSubFeature] = useState(subFeature);
  const [editedId, setEditedId] = useState(id);
  const [editedRequirement, setEditedRequirement] = useState(requirement);
  const [editedServicesToUse, setEditedServicesToUse] = useState(services_to_use || []);
  
  const onSave = () => {
    handleSave({
      feature: editedFeature,
      sub_feature: editedSubFeature,
      id: editedId,
      requirement: editedRequirement,
      services_to_use: editedServicesToUse,
      record_identifier:recordId,
    });
    handleClose();
  };

  const handleServiceChange = (index, value) => {
    const updatedServices = editedServicesToUse.map((service, i) => (i === index ? value : service));
    setEditedServicesToUse(updatedServices);
  };

  const handleAddService = () => {
    setEditedServicesToUse([...editedServicesToUse, '']);
  };

  const handleRemoveService = (index) => {
    const updatedServices = editedServicesToUse.filter((_, i) => i !== index);
    setEditedServicesToUse(updatedServices);
  };

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
      <DialogTitle>Edit Requirement</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="Feature"
          type="text"
          fullWidth
          variant="standard"
          value={editedFeature}
          onChange={(e) => setEditedFeature(e.target.value)}
          InputLabelProps={{
              style: { fontSize: '1.5rem' }, 
          }}
        />
        <TextField
          margin="dense"
          label="Sub Feature"
          type="text"
          fullWidth
          variant="standard"
          value={editedSubFeature}
          onChange={(e) => setEditedSubFeature(e.target.value)}
          InputLabelProps={{
              style: { fontSize: '1.5rem' }, 
          }}
        />
        <TextField
          margin="dense"
          label="ID"
          type="text"
          fullWidth
          variant="standard"
          value={editedId}
          onChange={(e) => setEditedId(e.target.value)}
          InputLabelProps={{
              style: { fontSize: '1.5rem' }, 
          }}
        />
        <TextField
          margin="dense"
          label="Requirement"
          type="text"
          fullWidth
          variant="standard"
          multiline
          rows={3}
          value={editedRequirement}
          onChange={(e) => setEditedRequirement(e.target.value)}
          InputLabelProps={{
              style: { fontSize: '1.5rem' }, 
          }}
        />
        <div>
        <br></br>
        <Typography variant="subtitle1">Define services you wish to include in your design</Typography>
          {editedServicesToUse.map((service, index) => (
            <div key={index} style={{ display: 'flex', alignItems: 'center', margin: '8px 0' }}>
              <TextField
                label={`Service ${index + 1}`}
                type="text"
                variant="standard"
                value={service}
                onChange={(e) => handleServiceChange(index, e.target.value)}
                style={{ flex: 1 }}
              />
              <IconButton onClick={() => handleRemoveService(index)}>
                <RemoveCircleOutlineIcon />
              </IconButton>
            </div>
          ))}
          <IconButton onClick={handleAddService}>
            <AddCircleOutlineIcon />
          </IconButton>
        </div>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={onSave}>Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default EditRequirementCardDialog;
