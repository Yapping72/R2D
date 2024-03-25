import React from 'react';
import { Button } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete'; 

const ClearIndexedDbButton = ({ repository }) => {
    const handleClearDatabase = async () => {
      try {
        await repository.handleClearDb(); // Call the clearDB function on the repository
        alert('Database cleared successfully');
      } catch (error) {
        console.error('Failed to clear database:', error);
        alert('Failed to clear database');
      }
    };
  
    return (
    <Button
        variant="outlined"
        startIcon={<DeleteIcon />} // Use the Delete icon as the startIcon of the Button
        onClick={handleClearDatabase}>
        Remove Uploaded Files
    </Button>
    );
};

export default ClearIndexedDbButton;