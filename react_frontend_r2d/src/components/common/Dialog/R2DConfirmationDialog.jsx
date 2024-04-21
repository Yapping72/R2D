import React from 'react';
import { Button, Typography, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';

/**
 * ConfirmationDialog presents a modal dialog to the user with options to confirm or cancel an action.
 *
 * @param {boolean} open Controls the visibility of the dialog; if true, the dialog is open.
 * @param {string} title The title of the dialog, displayed at the top.
 * @param {string} content The descriptive content inside the dialog prompting the user for confirmation.
 * @param {function} onConfirm The function to call when the user clicks the "Yes" button, confirming the action.
 * @param {function} onCancel The function to call when the user clicks the "No" button, cancelling the action.
 */

const R2DConfirmationDialog = ({ open, title, content, onConfirm, onCancel }) => {
  return (
      <Dialog
        open={open}
        onClose={onCancel}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
      <DialogTitle id="alert-dialog-title">{title}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          {content}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onCancel} color="primary">
          <Typography variant='button'> No</Typography>
        </Button>
        <Button onClick={onConfirm} color="primary" autoFocus>
        <Typography variant='button'> Yes</Typography>
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default R2DConfirmationDialog;
