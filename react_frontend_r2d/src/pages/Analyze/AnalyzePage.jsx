import React from 'react'
import {Container, Box, Typography} from '@mui/material'
import { useAlert } from '../../components/common/Alerts/AlertContext';
import UserStoryJobTable from '../../components/common/Jobs/UserStoryJobTable';


const AnalyzePage = () => {
    return(
        <Container>
        <Box>
            <Typography variant='h4'> Queue Jobs for Analysis </Typography>
            <h3> Add Tab here that switches between queue and results </h3>
            <Typography>Job Queue Table: 
            status: SENDING, SENT, PROCESSING, SUCCESS, ERROR</Typography>
            row actions: START JOB, CANCEL JOB, DOWNLOAD JOB PARAMETERS, VIEW JOB PARAMETERS
            table actions: ADD JOB TO QUEUE
            <h3>Second tab could be a mermaid renderer</h3>
        </Box>
        <UserStoryJobTable></UserStoryJobTable>
        </Container>
    )
}
export default AnalyzePage