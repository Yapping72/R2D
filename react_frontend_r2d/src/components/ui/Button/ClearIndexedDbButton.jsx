import React, { useState } from 'react';
import { Button } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import { useAlert } from '../../common/Alerts/AlertContext';
import R2DConfirmationDialog from '../../common/Dialog/R2DConfirmationDialog';

/**
 * ClearIndexedDbButton renders a button that, when clicked, prompts the user with a confirmation dialog
 * before proceeding to clear the IndexedDB.
 *
 * @param {object} repository An object that contains methods to interact with the IndexedDB.
 */

const ClearIndexedDbButton = ({ repository }) => {
    const [openConfirmDialog, setOpenConfirmDialog] = useState(false);
    const { showAlert } = useAlert();

    const handleClearDatabase = async () => {
        setOpenConfirmDialog(false); // Close the confirmation dialog first
        try {
            await repository.handleClearDb(); // Call the clearDB function on the repository
            showAlert('success', 'Your files have been successfully removed.');
        } catch (error) {
            console.error('Failed to clear database:', error);
            showAlert('error', 'An error was encountered while trying to remove uploaded files.');
        }
    };

    const handleOpenConfirmDialog = () => {
        setOpenConfirmDialog(true);
    };

    const handleCloseConfirmDialog = () => {
        setOpenConfirmDialog(false);
    };

    return (
        <>
            <Button
                variant="outlined"
                startIcon={<DeleteIcon />}
                onClick={handleOpenConfirmDialog}>
                Remove Uploaded Files
            </Button>
            <R2DConfirmationDialog
                open={openConfirmDialog}
                title="Confirm Deletion"
                content="Are you sure you want to remove all uploaded files?"
                onConfirm={handleClearDatabase}
                onCancel={handleCloseConfirmDialog}
            />
        </>
    );
};

export default ClearIndexedDbButton;
