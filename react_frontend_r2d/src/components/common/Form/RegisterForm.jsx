import { Typography, Avatar, Box, Container, TextField, Button, Grid, Link, FormControlLabel, Checkbox } from "@mui/material";
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import { WarningOutlined } from "@mui/icons-material";

import './RegisterForm.css';

/**
 * Renders a registration form triggers the registerUser function provided by parent
 * @param {Function} registerUser - function to invoke user registration
 * @returns 
 */
const RegisterForm = ({registerUser = (username, email, firstName, lastName, password, confirmPassword) => {}, errorMessage}) => {
    const handleRegister = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        registerUser(
            data.get('username'),
            data.get('email'),
            data.get('firstName'),
            data.get('lastName'),
            data.get('password'),
            data.get('confirmPassword'),
        )
    };

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
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                required
                                fullWidth
                                id="lastName"
                                label="Last Name"
                                name="lastName"
                                autoComplete="family-name"
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
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoComplete="username"
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        autoComplete="new-password"
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="confirmPassword"
                        label="Confirm Password"
                        type="password"
                        id="confirmPassword"
                        autoComplete="new-password"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
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
