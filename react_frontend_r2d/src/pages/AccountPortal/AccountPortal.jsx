import React, { useState } from 'react';
import { Switch, Box, Stack, Container } from '@mui/material';
import LoginForm from '../../components/common/Form/LoginForm';
import RegisterForm from '../../components/common/Form/RegisterForm';
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import LockOutlined from '@mui/icons-material/LockOutlined';

import ApiManager from '../../utils/Api/ApiManager';
import UrlsConfig from '../../utils/Api/UrlsConfig';
import { useAlert } from '../../components/common/Alerts/AlertContext';
import { PageNavigationService } from '../../utils/Pages/PageNavigationService';
import { ROUTES } from '../../utils/Pages/RoutesConfig';

const AccountPortalPage = () => {
    const [isLoginForm, setIsLoginForm] = useState(true);
    const { showAlert } = useAlert();
    const { navigateTo } = PageNavigationService();
    const [errorMessage, setErrorMessage] = useState('');

    const handleToggle = (event) => {
        setIsLoginForm(event.target.checked);
    };

    /**
     * Retrieves the username and password field form the login form and passes it to the login endpoint.
     * Triggers the login flow, if valid credentials are provided, users are redirected to otp page.
     * @param {String} username Username to authenticate a user
     * @param {String} password Password to authenticate a user
     */
    const loginUser = async (username, password) => {
        console.debug(`Username and password: ${username}, ${password}`)
        // Create the payload data 
        const requestPayload = {
            "username": username,
            "password": password
        }
        try {
            const result = await ApiManager.postData(UrlsConfig.endpoints.LOGIN, requestPayload);
            if (result.success) {
                console.debug(`${username}, ${password}, ${result.data.user_id} - Login successful, proceeding to OTP`);
  
                navigateTo(ROUTES.OTP, { userId: result.data.user_id, email: result.data.user_email}); // Pass userId as state
            } else {
                // Set error message
                setErrorMessage('Incorrect username or password provided. Note that your account will be disabled after 5 invalid login attempts.');
            }
        } catch (error) {
            // Handle unexpected errors
            console.error('Login Error:', error);
            showAlert("error", "An unexpected error occurred while trying to sign you in")
        }
    }

    const registerUser = async (username, email, firstName, lastName, password, confirmPassword) => {
        console.log(`${username}, ${email}, ${firstName}, ${lastName}, ${password}, ${confirmPassword}`)
        // Create the payload data 
        const requestPayload = {
            "username": username,
            "password": password,
            "email":email,
            "first_name":firstName,
            "last_name":lastName,
            "password":password,
            "confirmPassword":confirmPassword
        }
        try {
            const result = await ApiManager.postData(UrlsConfig.endpoints.REGISTER, requestPayload);
            if (result.success) {
                console.debug(`${username}, ${password}, ${result.access_token} - Login successful, proceeding to OTP`);
            } else {
                // Set error message
                setErrorMessage(`${result.message}`);
            }
        } catch (error) {
            // Handle unexpected errors
            console.error('Registration Error:', error);
            showAlert("error", "An unexpected error occurred while trying to register your account.")
        }
    }

    return (
        <Container>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                {/* Form Container with reduced margin */}
                <Box sx={{ width: '100%', transition: 'transform 0.3s', mt: -1 }}>
                    <Stack direction="row" spacing={0} alignItems="center" justifyContent="center" sx={{ mb: -8 }}>
                        <AppRegistrationIcon color="action" />
                        <Switch checked={isLoginForm} onChange={handleToggle} />
                        <LockOutlined color="action" />
                    </Stack>
                    {isLoginForm ? <LoginForm loginUser={loginUser} errorMessage={errorMessage}></LoginForm> : <RegisterForm registerUser={registerUser}  errorMessage={errorMessage}></RegisterForm>}
                </Box>
            </Box>
        </Container>
    );
};

export default AccountPortalPage;
