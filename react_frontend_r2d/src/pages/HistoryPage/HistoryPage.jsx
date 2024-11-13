import React, {useState, useEffect} from 'react'
import { Box, Tabs, Tab, Divider, Container, Typography } from '@mui/material'
import { useAlert } from '../../components/common/Alerts/AlertContext';
import HistoryTable from '../../components/common/Tables/HistoryTable';
import ApiManager from '../../utils/Api/ApiManager';
import UrlsConfig from '../../utils/Api/UrlsConfig';


const HistoryPage = () => {
// State to store the fetched job history data
const [jobHistory, setJobHistory] = useState([]);
const { showAlert } = useAlert();

// useEffect to fetch job history data from the API on component mount
useEffect(() => {
    const fetchJobHistory = async () => {
            try {
                const serverResponse = await ApiManager.postData(UrlsConfig.endpoints.GET_JOB_HISTORY, {});           
                if (serverResponse.success) {
                    setJobHistory(serverResponse.data.job_history); // Set fetched data to state
                    showAlert('success', 'Successfully retrieved job history data.');
                } else {
                    showAlert('error', 'Failed to retrieve job history data.');
                }
            } catch (error) {
                showAlert('error', 'An error occurred while fetching job history data.');
            }
        };

        fetchJobHistory();
    }, []); 


    return (
            <Container>
            <Typography variant='h4'>Job History</Typography>
            <Divider sx={{ my: 2 }} />
                <Box>
                    <HistoryTable
                        jobHistory={jobHistory}
                    ></HistoryTable>
                </Box>
            </Container>
    )
}
export default HistoryPage