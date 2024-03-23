// SettingsNavigation.js
import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';

function SettingsNavigation({ settings, handleCloseNavMenu }) {
  return (
    <>
      {settings.map((setting) => (
        <MenuItem key={setting} onClick={handleCloseNavMenu}>
          <Button href={`/${setting.toLowerCase().replace(/\s/g, '-')}`} color="inherit">
            {setting}
          </Button>
        </MenuItem>
      ))}
    </>
  );
}

export default SettingsNavigation;
