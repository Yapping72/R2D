import React, {useState, useEffect} from 'react'
import { Box, Tabs, Tab, Divider, Container, Typography } from '@mui/material'
import { useAlert } from '../../components/common/Alerts/AlertContext';
import HistoryTable from '../../components/common/Tables/HistoryTable';

const jobHistoryData = 
[
  {
    "job_id": "0bb9c174-d79d-496f-ba68-ac47998379be",
    "previous_status": "Processing",
    "current_status": "Completed",
    "job_type": "class_diagram",
    "created_timestamp": "2024-11-06T02:46:02.082565+08:00",
    "last_updated_timestamp": "2024-11-06T02:46:02.082577+08:00"
  },
  {
    "job_id": "36accd69-1750-465e-a767-5456f294aca0",
    "previous_status": "Processing",
    "current_status": "Completed",
    "job_type": "er_diagram",
    "created_timestamp": "2024-11-06T02:46:02.019609+08:00",
    "last_updated_timestamp": "2024-11-06T02:46:02.019621+08:00"
  },
  {
    "job_id": "d7c0c150-5ab7-4f4f-aac5-11b18abd14db",
    "previous_status": "Processing",
    "current_status": "Completed",
    "job_type": "sequence_diagram",
    "created_timestamp": "2024-11-06T02:46:01.909622+08:00",
    "last_updated_timestamp": "2024-11-06T02:46:01.909632+08:00"
  },
  {
    "job_id": "d7c0c150-5ab7-4f4f-aac5-11b18abd14db",
    "previous_status": "Submitted",
    "current_status": "Processing",
    "job_type": "sequence_diagram",
    "created_timestamp": "2024-11-06T02:45:34.270970+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:34.270986+08:00"
  },
  {
    "job_id": "36accd69-1750-465e-a767-5456f294aca0",
    "previous_status": "Completed",
    "current_status": "Processing",
    "job_type": "er_diagram",
    "created_timestamp": "2024-11-06T02:45:34.211684+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:34.211705+08:00"
  },
  {
    "job_id": "d7c0c150-5ab7-4f4f-aac5-11b18abd14db",
    "previous_status": null,
    "current_status": "Submitted",
    "job_type": "sequence_diagram",
    "created_timestamp": "2024-11-06T02:45:34.115531+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:34.115549+08:00"
  },
  {
    "job_id": "36accd69-1750-465e-a767-5456f294aca0",
    "previous_status": "Processing",
    "current_status": "Completed",
    "job_type": "er_diagram",
    "created_timestamp": "2024-11-06T02:45:33.758580+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:33.758604+08:00"
  },
  {
    "job_id": "36accd69-1750-465e-a767-5456f294aca0",
    "previous_status": "Submitted",
    "current_status": "Processing",
    "job_type": "er_diagram",
    "created_timestamp": "2024-11-06T02:45:03.452975+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:03.453009+08:00"
  },
  {
    "job_id": "0bb9c174-d79d-496f-ba68-ac47998379be",
    "previous_status": "Completed",
    "current_status": "Processing",
    "job_type": "class_diagram",
    "created_timestamp": "2024-11-06T02:45:03.383342+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:03.383363+08:00"
  },
  {
    "job_id": "36accd69-1750-465e-a767-5456f294aca0",
    "previous_status": null,
    "current_status": "Submitted",
    "job_type": "er_diagram",
    "created_timestamp": "2024-11-06T02:45:03.304733+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:03.304752+08:00"
  },
  {
    "job_id": "0bb9c174-d79d-496f-ba68-ac47998379be",
    "previous_status": "Processing",
    "current_status": "Completed",
    "job_type": "class_diagram",
    "created_timestamp": "2024-11-06T02:45:03.100079+08:00",
    "last_updated_timestamp": "2024-11-06T02:45:03.100096+08:00"
  },
  {
    "job_id": "0bb9c174-d79d-496f-ba68-ac47998379be",
    "previous_status": "Submitted",
    "current_status": "Processing",
    "job_type": "class_diagram",
    "created_timestamp": "2024-11-06T02:44:31.675865+08:00",
    "last_updated_timestamp": "2024-11-06T02:44:31.675881+08:00"
  },
  {
    "job_id": "0bb9c174-d79d-496f-ba68-ac47998379be",
    "previous_status": null,
    "current_status": "Submitted",
    "job_type": "class_diagram",
    "created_timestamp": "2024-11-06T02:44:31.547621+08:00",
    "last_updated_timestamp": "2024-11-06T02:44:31.547634+08:00"
  }
]

const HistoryPage = () => {
    return (
            <Container>
            <Typography variant='h4'>Job History</Typography>
            <Divider sx={{ my: 2 }} />
                <Box>
                    <HistoryTable
                        jobHistory={jobHistoryData}
                    ></HistoryTable>
                </Box>
            </Container>
    )
}
export default HistoryPage