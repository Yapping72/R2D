import React from 'react';
import {Box, Typography, Button} from '@mui/material'
import { PageNavigationService } from '../../utils/Pages/PageNavigationService';
import { ROUTES } from '../../utils/Pages/RoutesConfig';

const LogoutPage = () => {
    const { navigateTo } = PageNavigationService();

    const navigateToHome = () => {
        navigateTo(ROUTES.HOME)
    }

    const navigateToAccountPortal = () => {
        navigateTo(ROUTES.ACCOUNT_PORTAL)
    }

    return (
        <Box textAlign="center" mt={20}>
            <Typography variant='h4'>You have been successfully logged out</Typography>
            <Typography variant='h5'>We hope to see you again</Typography>
            <Button onClick={()=>navigateToHome()}>To Home</Button>
            <Button onClick={()=>navigateToAccountPortal()}>Jump Back In</Button>
        </Box>
    )       
}

export default LogoutPage