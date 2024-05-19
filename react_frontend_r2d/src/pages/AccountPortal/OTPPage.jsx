import React from 'react'
import OTPForm from '../../components/common/Form/OTPForm'
import { Box } from '@mui/material';

/**
 * Renders an OTP form and is responsible for triggering the OTP authentication flow.
 * @returns 
 */
const OTPPage = () => {
    const performOTPVerification = (otp) => {
        console.log(`Your OTP you submitted: ${otp}`)
    }

    return(
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="70vh">
            <OTPForm performOTPVerification={performOTPVerification}/>
        </Box>
    )
}

export default OTPPage