// MenuNavigation.js
import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';

function MenuNavigation({ pages, handleCloseNavMenu }) {
  return (
    <>
      {pages.map((page) => (
        <MenuItem key={page} onClick={handleCloseNavMenu}>
          <Button href={`/${page}`} color="inherit">
            {page}
          </Button>
        </MenuItem>
      ))}
    </>
  );
}

export default MenuNavigation;
