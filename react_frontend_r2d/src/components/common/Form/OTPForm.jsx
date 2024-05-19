import React, { useState, useEffect } from 'react';
import { Container, Grid, TextField, Typography, Box, Stack } from '@mui/material';
import { styled } from '@mui/material/styles';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

/**
 * OTP Input field that is rendered by the OTPForm
 */
const OTPInput = styled(({ valid, ...other }) => <TextField {...other} />)(({ valid }) => ({
  '& input': {
    textAlign: 'center',
    fontSize: '3rem',
    width: '80px',
    height: '80px',
    color: 'white',
    backgroundColor: 'black',
  },
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: valid === null ? 'white' : valid ? 'green' : 'red',
    },
    '&:hover fieldset': {
      borderColor: valid === null ? 'white' : valid ? 'darkgreen' : 'darkred',
    },
    '&.Mui-focused fieldset': {
      borderColor: valid === null ? 'white' : valid ? 'green' : 'red',
    },
  },
}));

/**
 * OTP Form that renders 8 OTP Inputs by default. Accepts a performOTPVerification function.
 * The form will be disabled after 10mins (OTP duration)
 */
const OTPForm = ({ performOTPVerification = (otp) => {console.log(otp)}, numberOfBoxes = 8 }) => {
  const [otp, setOtp] = useState(Array(numberOfBoxes).fill(''));
  const [validity, setValidity] = useState(Array(numberOfBoxes).fill(null)); // null for blank, true for valid, false for invalid
  const [timeLeft, setTimeLeft] = useState(600); // 600 seconds = 5 minutes
  const [isDisabled, setIsDisabled] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTimeLeft((prevTime) => {
        if (prevTime <= 1) {
          clearInterval(intervalId);
          setIsDisabled(true); // Disable the inputs when the time is up
          return 0;
        }
        return prevTime - 1;
      });
    }, 1000);
    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    const firstEmptyIndex = otp.findIndex((val) => val === '');
    if (firstEmptyIndex !== -1) {
      document.getElementById(`otp-${firstEmptyIndex}`).focus();
    }
  }, [otp]);
  const onComplete = (otp) => {
    performOTPVerification(otp);
  }

  const handleInputChange = (index) => (e) => {
    const value = e.target.value;
    if (/^\d$/.test(value)) {
      // Only allow numeric values
      const newOtp = [...otp];
      newOtp[index] = value;
      setOtp(newOtp);

      const newValidity = [...validity];
      newValidity[index] = true;
      setValidity(newValidity);

      if (index < numberOfBoxes - 1) {
        document.getElementById(`otp-${index + 1}`).focus();
      }

      if (newOtp.every((val) => val !== '')) {
        onComplete(newOtp.join(''));
      }
    }
  };

  const handleKeyDown = (index) => (e) => {
    if (e.key === 'Backspace') {
      const newOtp = [...otp];
      const newValidity = [...validity];

      if (otp[index] === '') {
        if (index > 0) {
          newOtp[index - 1] = '';
          newValidity[index - 1] = null;
          setOtp(newOtp);
          setValidity(newValidity);
          document.getElementById(`otp-${index - 1}`).focus();
        }
      } else {
        newOtp[index] = '';
        newValidity[index] = null;
        setOtp(newOtp);
        setValidity(newValidity);
      }
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `OTP expires in ${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
  };

  return (
    <Container>
      <Stack spacing={2} alignItems="center">
        <Box textAlign="center">
          <Typography variant='h4'>OTP Verification</Typography>
          <Typography variant='subtitle1'>A one-time password has been sent to your registered email account.</Typography>
        </Box>
        <Grid container spacing={2} justifyContent="center">
          {otp.map((value, index) => (
            <Grid item key={index}>
              <OTPInput
                id={`otp-${index}`}
                variant="outlined"
                value={value}
                onChange={handleInputChange(index)}
                onKeyDown={handleKeyDown(index)}
                inputProps={{ maxLength: 1, inputMode: 'numeric', pattern: '[0-9]*' }}
                disabled={isDisabled}
                valid={validity[index]}
              />
            </Grid>
          ))}
        </Grid>
        <Box display="flex" justifyContent="center" alignItems="center">
          <AccessTimeIcon color="secondary" />
          <Typography variant="h6" color="secondary" ml={1}>
            {formatTime(timeLeft)}
          </Typography>
        </Box>
      </Stack>
    </Container>
  );
};

export default OTPForm;
