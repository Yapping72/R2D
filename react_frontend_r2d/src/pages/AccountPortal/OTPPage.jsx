import React, {useState} from 'react'
import OTPForm from '../../components/common/Form/OTPForm'
import { Box } from '@mui/material';
import { useLocation } from 'react-router-dom';
import ApiManager from '../../utils/Api/ApiManager';
import UrlsConfig from '../../utils/Api/UrlsConfig';
import { useAlert } from '../../components/common/Alerts/AlertContext';
import { PageNavigationService } from '../../utils/Pages/PageNavigationService';
import { ROUTES } from '../../utils/Pages/RoutesConfig';
import JwtHandler from '../../utils/Jwt/JwtHandler';
import { useAuth } from '../../components/common/Authentication/AuthContext';

/**
 * Renders an OTP form and is responsible for triggering the OTP authentication flow.
 * After successful login, user id is return. 
 * OTP authentication flow expects user_id + otp in request payload
 * @returns 
 */
const OTPPage = () => {
    const location = useLocation();
    const { userId, email } = location.state || {};
    const { showAlert } = useAlert();
    const { navigateTo } = PageNavigationService();
    const [errorMessage, setErrorMessage] = useState('');
    const { setLoginAndStartInactivityTimer } = useAuth();
    /**
     * Triggers the OTP authentication flow.
     * BE otp authentication relies on userId and otp 
     * @param {*} otp 
     */
    const performOTPVerification =  async (otp) => {
        console.debug(`${otp}, ${userId}`)
        // Create the payload data 
        const requestPayload = {
            "user_id": userId, 
            "otp":otp
        }
        try {
            const result = await ApiManager.postData(UrlsConfig.endpoints.OTP, requestPayload);
            if (result.success) {
                console.debug(`${otp} ${result.data.access_token} - Login successful, proceeding to OTP`);
                showAlert("success", "Welcome back !");
                JwtHandler.setToken(result.data.access_token)
                setLoginAndStartInactivityTimer();
                navigateTo(ROUTES.UPLOAD); // Pass userId as state
                return true;
            } else {
                setErrorMessage('Incorrect OTP provided. Note that your account will be disabled after 5 invalid login attempts.');
                return false;
            }
        } catch (error) {
            // Handle unexpected errors
            console.error('OTP Error:', error);
            showAlert("error", "An unexpected error occurred while trying to sign you in");
            return false;
        }
    }

    return(
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh">
            <OTPForm performOTPVerification={performOTPVerification} errorMessage={errorMessage} email = {email} numberOfBoxes={8}/>
        </Box>
    )
}

export default OTPPage