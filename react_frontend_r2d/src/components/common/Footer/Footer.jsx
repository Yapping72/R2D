import React from 'react';
import { AppBar, Toolbar, Typography, IconButton } from '@mui/material';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import GitHubIcon from '@mui/icons-material/GitHub';

const Footer = () => {
  return (
        <AppBar position="relative" color="transparent">
            <Toolbar sx={{ justifyContent: 'space-between' }}>
              <Typography variant="subtitle2" color="inherit">
                &copy; 2024 Requirements2Design. All rights reserved.
              </Typography>
              <div>
                <IconButton
                  aria-label="LinkedIn"
                  color="inherit"
                  href="https://www.linkedin.com/in/yap-ping-119732236"
                  rel="noopener noreferrer"
                  target="_blank">
                  <LinkedInIcon />
                </IconButton>

                <IconButton
                  aria-label="GitHub"
                  color="inherit"
                  href="https://github.com/Yapping72"
                  rel="noopener noreferrer"
                  target="_blank">
                  <GitHubIcon />
                </IconButton>
              </div>
            </Toolbar>
          </AppBar>
  );
};

export default Footer;
