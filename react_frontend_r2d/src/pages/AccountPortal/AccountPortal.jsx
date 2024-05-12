import React, { useState } from 'react';
import { Switch, Box, Typography, Stack, Container } from '@mui/material';
import LoginForm from '../../components/common/Form/LoginForm';
import RegisterForm from '../../components/common/Form/RegisterForm';
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import LockOutlined from '@mui/icons-material/LockOutlined';

const AccountPortalPage = () => {
    const [isLoginForm, setIsLoginForm] = useState(true);

    const handleToggle = (event) => {
        setIsLoginForm(event.target.checked);
    };

    return (
        <Container>
        <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            {/* Form Container with reduced margin */}
            <Box sx={{ width: '100%', transition: 'transform 0.3s', mt:-1}}>
            <Stack direction="row" spacing={0} alignItems="center" justifyContent="center" sx={{mb:-8}}>
                <AppRegistrationIcon color="action" />
                <Switch checked={isLoginForm} onChange={handleToggle} />
                <LockOutlined color="action" />
            </Stack>
                {isLoginForm ? <LoginForm /> : <RegisterForm />}
            </Box>
        </Box>
        </Container>
    );
};

export default AccountPortalPage;
