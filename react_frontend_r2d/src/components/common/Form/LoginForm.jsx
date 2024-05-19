import { Typography, Avatar, Box, Container, Checkbox, Grid, Link, FormControlLabel, FormLabel, TextField, Button} from "@mui/material"
import LockOutlined from '@mui/icons-material/LockOutlined';
import { WarningOutlined } from "@mui/icons-material";
import './LoginForm.css'

/**
 * Login form 
 * @param {function} loginUser - Function that takes in username and password and logs in a user
 * @returns 
 */
const LoginForm = ({loginUser = (username, password) => {console.log(username, password)}, errorMessage}) => {

    const handleLogin = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        loginUser(data.get('username'), data.get('password'));
      };

    return (
        <Container maxWidth="xs">
        <Box
          className='login-form-container'
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx = {{bgcolor: 'primary.main'}}>
          <LockOutlined />
          </Avatar>
          <Typography component="h1" variant="h5">
          Login
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
          <Box component="form" onSubmit={handleLogin} noValidate sx={{ mt: 1 }}>
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
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
            <Typography>LOGIN</Typography>
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="#s" variant="body2">
                 <Typography>Forgot password?</Typography> 
                </Link>
              </Grid>
              <Grid item>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    );
}

export default LoginForm