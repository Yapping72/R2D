import React, { useState } from 'react';
import {Switch, Box, Stack, Tooltip } from '@mui/material';
import LoginForm from '../../components/common/Form/LoginForm';
import RegisterForm from '../../components/common/Form/RegisterForm';
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import LockOutlined from '@mui/icons-material/LockOutlined';

import ApiManager from '../../utils/Api/ApiManager';
import UrlsConfig from '../../utils/Api/UrlsConfig';
import { useAlert } from '../../components/common/Alerts/AlertContext';
import { PageNavigationService } from '../../utils/Pages/PageNavigationService';
import { ROUTES } from '../../utils/Pages/RoutesConfig';
import JwtHandler from '../../utils/Jwt/JwtHandler';
import { useAuth } from '../../components/common/Authentication/AuthContext';
import TimedBackdrop from '../../components/common/Backdrops/TimedBackdrop';

const AccountPortalPage = () => {
    const [isLoginForm, setIsLoginForm] = useState(true);
    const { showAlert } = useAlert();
    const { navigateTo } = PageNavigationService();
    const [errorMessage, setErrorMessage] = useState('');
    const { setLoginAndStartInactivityTimer } = useAuth();
    const [showBackdrop, setShowBackdrop] = useState(false);

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
                navigateTo(ROUTES.OTP, { userId: result.data.user_id, email: result.data.user_email }); // Pass userId as state
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
    /**
     * Retrieves registration details and attempts to registers a user
     * Triggers the registration flow, if account successfully registered, users are redirected to upload page and access token stored in local storage.
     * @param {String} username Username to register a user
     * @param {String} email email to register a user
     * @param {String} firstName first name to register a user
     * @param {String} lastName last name to register a user
     * @param {String} password password to register a user
     * @param  {String} confirmPassword confirm password to register a user
     */
    const registerUser = async (registrationData) => {
        // Create the payload data 
        const requestPayload = {
            "username": registrationData.username,
            "email": registrationData.email,
            "preferred_name": registrationData.preferredName || registrationData.username, 
            "first_name": registrationData.firstName,
            "last_name": registrationData.lastName || "", 
            "password": registrationData.password,
            "confirmPassword": registrationData.confirmPassword
        }

        try {
            const result = await ApiManager.postData(UrlsConfig.endpoints.REGISTER, requestPayload);
            if (result.success) {
                console.debug(`${result.data}`);
                JwtHandler.setToken(result.data.access_token);
                setLoginAndStartInactivityTimer();
                setShowBackdrop(true); // Show the backdrop
                setTimeout(() => {
                    setShowBackdrop(false);
                    navigateTo(ROUTES.UPLOAD);
                }, 1000);
            } else {
                setErrorMessage(`${result.message}`);
            }
        } catch (error) {
            // Handle unexpected errors
            console.error('Registration Error:', error);
            showAlert("error", "An unexpected error occurred while trying to register your account.")
        }
    }

    return (
        <Box>
            <Box sx={{ width: '100%', transition: 'transform 0.3s', mt: isLoginForm ? 11 : 5, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Stack direction="row" spacing={0} alignItems="center" justifyContent="center" sx={{ mb: isLoginForm ? -8 : -8 }}>
                    <Tooltip title="Select to register for an account!">
                        <AppRegistrationIcon />
                    </Tooltip>
                    <Switch checked={isLoginForm} onChange={handleToggle} />
                    <Tooltip title="Select to login to your account!">
                        <LockOutlined />
                    </Tooltip>
                </Stack>
                    {isLoginForm ? (
                        <LoginForm loginUser={loginUser} errorMessage={errorMessage}/>
                    ) : (
                        <RegisterForm registerUser={registerUser} errorMessage={errorMessage} />
                    )}
            </Box>
            <TimedBackdrop open={showBackdrop} onClose={() => setShowBackdrop(false)} duration={1000} />
        </Box>
    );
};

export default AccountPortalPage;
