import { Typography, Avatar, Box, Paper, Container, Checkbox, Grid, Link, FormControlLabel, FormLabel, TextField, Button} from "@mui/material"
import LockOutlined from '@mui/icons-material/LockOutlined';
import './LoginForm.css'

const LoginForm = () => {
    const handleLogin = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        console.log({
          email: data.get('email'),
          password: data.get('password'),
        });
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