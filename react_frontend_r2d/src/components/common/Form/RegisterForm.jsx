import React, { useState, useEffect } from 'react';
import { Typography, Avatar, Box, Container, TextField, Button, Grid, Link, Tooltip, IconButton, InputAdornment } from "@mui/material";
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import { WarningOutlined, Visibility, VisibilityOff } from "@mui/icons-material";
import InputValidator from '../../../utils/Validators/InputValidator';

import './RegisterForm.css';

/**
 * Renders a registration form triggers the registerUser function provided by parent
 * @param {Function} registerUser - function to invoke user registration
 * @returns 
 */

const RegisterForm = ({ registerUser = (registrationData) => { }, errorMessage }) => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        firstName: '',
        lastName: '',
        password: '',
        confirmPassword: '',
        preferredName: ''
    });
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});
    const [isFormValid, setIsFormValid] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const handleBlur = (field) => (e) => {
        setTouched({ ...touched, [field]: true });
        const { name, value } = e.target;
        const error = validate(name, value, formData);
        setErrors({ ...errors, [name]: error });
    };

    const validate = (name, value, formData) => {
        switch (name) {
            case 'username':
                if (!InputValidator.isValidUsername(value)) {
                    return 'Username must be alphanumeric and between 9 and 64 characters, with at least one digit';
                }
                break;
            case 'preferredName':
                if (!InputValidator.isValidPreferredName(value)) {
                    return 'Display name may be alphanumeric and between 3 and 64 characters';
                }
                break;
            case 'email':
                if (!InputValidator.isValidEmail(value)) {
                    return 'Invalid email address';
                }
                break;
            case 'password':
                if (!InputValidator.isValidPassword(value)) {
                    return 'Password must be between 12 and 128 characters';
                }
                break;
            case 'confirmPassword':
                console.log('Password:', formData.password, 'Value:', value)
                if (!InputValidator.doPasswordsMatch(formData.password, value)) {
                    return 'Passwords do not match';
                }
                break;
            case 'firstName':
                if (!InputValidator.isNonEmpty(value)) {
                    return 'First Name is required';
                }
                break;
            default:
                return '';
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        const updatedFormData = { ...formData, [name]: value };
        setFormData(updatedFormData);
        const error = validate(name, value, updatedFormData);
        setErrors((prevErrors) => ({ ...prevErrors, [name]: error }));

        // Validate confirm password whenever password changes
        if (name === 'password' || name === 'confirmPassword') {
            const confirmPasswordError = validate('confirmPassword', updatedFormData.confirmPassword, updatedFormData);
            setErrors((prevErrors) => ({ ...prevErrors, confirmPassword: confirmPasswordError }));
        }

        validateForm(updatedFormData);
    };

    const validateForm = () => {
        const fields = ['username', 'email', 'firstName', 'lastName', 'preferredName', 'password', 'confirmPassword'];
        let isValid = true;

        fields.forEach((name) => {
            const value = formData[name];
            const error = validate(name, value, formData);
            if (error) {
                isValid = false;
            }
        });

        setIsFormValid(isValid);
    };

    const validateInputs = () => {
        const errors = {};
        let isValid = true;

        ['username', 'email', 'firstName', 'lastName', 'password', 'confirmPassword', 'preferredName'].forEach((name) => {
            const value = formData[name];
            const error = validate(name, value, formData);
            if (error) {
                errors[name] = error;
                isValid = false;
            }
        });

        setErrors(errors);
        return isValid;
    };

    const handleClickShowPassword = () => setShowPassword((show) => !show);
    const handleClickShowConfirmPassword = () => setShowConfirmPassword((show) => !show);


    const handleRegister = (event) => {
        event.preventDefault();
        if (validateInputs()) {
            // Prepare registration data to send to the parent component
            const registrationData = { 
                username: formData.username,
                email: formData.email,
                firstName: formData.firstName,
                lastName: formData.lastName,
                password: formData.password,
                confirmPassword: formData.confirmPassword,
                preferredName: formData.preferredName
            }
            // Invoke the registerUser function provided by the parent component
            registerUser(registrationData);
        }
    };

    useEffect(() => {
        validateForm();
    }, [formData]);

    return (
        <Container maxWidth="xs">
            <Box
                className='register-form-container'
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    padding: 2,
                    borderRadius: 2,
                    boxShadow: 3
                }}
            >
                <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
                    <AppRegistrationIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Register
                </Typography>
                {errorMessage && (
                    <Box sx={{
                        mt: 2,
                        p: 2,
                        borderRadius: 1,
                        bgcolor: 'rgba(244, 67, 54, 0.15)', // Slightly transparent red
                        color: 'error.main',
                        border: '1px solid',
                        borderColor: 'error.dark', // Darker shade of red for the border
                        display: 'flex',
                        alignItems: 'center',
                        width: '100%'
                    }}>
                        <WarningOutlined sx={{ mr: 1 }} /> {/* Warning icon */}
                        <Typography>{errorMessage}</Typography>
                    </Box>
                )}
                <Box component="form" onSubmit={handleRegister} noValidate sx={{ mt: 2 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                required
                                fullWidth
                                id="firstName"
                                label="First Name"
                                name="firstName"
                                autoComplete="given-name"
                                onBlur={handleBlur('firstName')}
                                onChange={handleChange}
                                error={touched.firstName && Boolean(errors.firstName)}
                                helperText={touched.firstName && errors.firstName}
                                inputProps={{ maxLength: 64 }}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                fullWidth
                                id="lastName"
                                label="Last Name"
                                name="lastName"
                                autoComplete="family-name"
                                onBlur={handleBlur('lastName')}
                                onChange={handleChange}
                                error={touched.lastName && Boolean(errors.lastName)}
                                helperText={touched.lastName && errors.lastName}
                                inputProps={{ maxLength: 64 }}
                            />
                        </Grid>
                    </Grid>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="email"
                        label="Email Address"
                        name="email"
                        type="email"
                        autoComplete="email"
                        onBlur={handleBlur('email')}
                        onChange={handleChange}
                        error={touched.email && Boolean(errors.email)}
                        helperText={touched.email && errors.email}
                        inputProps={{ maxLength: 254 }}
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoComplete="username"
                        onBlur={handleBlur('username')}
                        onChange={handleChange}
                        error={touched.username && Boolean(errors.username)}
                        helperText={touched.username && errors.username}
                        inputProps={{ minLength: 9, maxLength: 64 }}
                    />
                    <Tooltip title="We recommend setting a display name that does not reveal personal information about yourself">
                        <TextField
                            margin="normal"
                            fullWidth
                            id="preferredName':"
                            label="Display Name"
                            name='preferredName'
                            onBlur={handleBlur('preferredName')}
                            onChange={handleChange}
                            error={touched.preferredName && Boolean(errors.preferredName)}
                            helperText={touched.preferredName && errors.preferredName}
                            inputProps={{ minLength: 9, maxLength: 64 }}
                        />
                    </Tooltip>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type={showPassword ? 'text' : 'password'}
                        id="password"
                        autoComplete="new-password"
                        onBlur={handleBlur('password')}
                        onChange={handleChange}
                        error={touched.password && Boolean(errors.password)}
                        helperText={touched.password && errors.password}
                        inputProps={{ minLength: 12, maxLength: 128 }}
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label="toggle password visibility"
                                        onClick={handleClickShowPassword}
                                        edge="end"
                                    >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />

                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="confirmPassword"
                        label="Confirm Password"
                        type={showConfirmPassword ? 'text' : 'password'}
                        id="confirmPassword"
                        autoComplete="new-password"
                        onBlur={handleBlur('confirmPassword')}
                        onChange={handleChange}
                        error={touched.confirmPassword && Boolean(errors.confirmPassword)}
                        helperText={touched.confirmPassword && errors.confirmPassword}
                        inputProps={{ minLength: 12, maxLength: 128 }}
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label="toggle confirm password visibility"
                                        onClick={handleClickShowConfirmPassword}
                                        edge="end"
                                    >
                                        {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                        disabled={!isFormValid} // Disable button if form is not valid
                    >
                        <Typography>Register</Typography>
                    </Button>
                    <Grid container justifyContent="flex-end">
                        <Grid item>
                            <Link href="/login" variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Container>
    );
};

export default RegisterForm;