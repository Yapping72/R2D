// SettingsNavigation.js
import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';
import { useAuth } from '../Authentication/AuthContext';


function SettingsNavigation({ settings, handleCloseNavMenu }) {
  const { logout } = useAuth(); // Get the logout function from AuthContext

  const handleMenuItemClick = (setting) => {
    if (setting === 'Logout' || setting === 'logout') {
      logout();
    }
    handleCloseNavMenu();
  };

  return (
    <>
      {settings.map((setting) => (
        <MenuItem key={setting} onClick={() => handleMenuItemClick(setting)}>
          <Button href={`/${setting.toLowerCase().replace(/\s/g, '-')}`} color="inherit">
            {setting}
          </Button>
        </MenuItem>
      ))}
    </>
  );
}

export default SettingsNavigation;
