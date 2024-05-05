import React, { useState } from 'react';
import { Switch, Box, Typography, Stack } from '@mui/material';
import LoginForm from '../../components/common/Form/LoginForm';
import RegisterForm from '../../components/common/Form/RegisterForm';
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import LockOutlined from '@mui/icons-material/LockOutlined';
import TypingAnimation from '../../components/common/Animations/TypingAnimation';

const AccountPortalPage = () => {
    const [isLoginForm, setIsLoginForm] = useState(true);

    const handleToggle = (event) => {
        setIsLoginForm(event.target.checked);
    };

    return (
        <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 0}}>
            <Typography variant="h4" gutterBottom >
                {isLoginForm ? <TypingAnimation text = "Start Designing" variant='h4'></TypingAnimation> : <TypingAnimation text = "Create your R2D Account" variant='h4'></TypingAnimation> }
            </Typography>
            <Stack direction="row" spacing={1} alignItems="center" justifyContent="center" sx={{ mb: 2 }}>
                <AppRegistrationIcon color="action" />
                <Switch checked={isLoginForm} onChange={handleToggle} />
                <LockOutlined color="action" />
            </Stack>
            {/* Form Container with reduced margin */}
            <Box sx={{ width: '100%', mt: -8, transition: 'transform 0.3s' }}>
                {isLoginForm ? <LoginForm /> : <RegisterForm />}
            </Box>
        </Box>
    );
};

export default AccountPortalPage;
