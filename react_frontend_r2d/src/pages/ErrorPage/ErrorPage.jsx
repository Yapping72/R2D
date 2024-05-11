import React from 'react';
import { Stack, Button, Typography, Container } from '@mui/material';
import { ROUTES } from '../../utils/Pages/RoutesConfig'; // Ensure correct path
import { PageNavigationService } from '../../utils/Pages/PageNavigationService';

export const ErrorPage = ({ errorCode = "404", errorMessage = "Oops, the requested page was not found.", redirectToPage = ROUTES.HOME }) => {
    const {navigateTo} = PageNavigationService();

    return (
        <Container style={{ height: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Stack spacing={1} textAlign="center"> 
                <Typography variant="h1" gutterBottom>{errorCode}</Typography>
                <Typography variant="subtitle1" gutterBottom>{errorMessage}</Typography>
                <Button variant="outlined" color="primary" onClick={() => navigateTo(redirectToPage)}>
                    Go Back
                </Button>
            </Stack>
        </Container>
    );
};

export default ErrorPage
