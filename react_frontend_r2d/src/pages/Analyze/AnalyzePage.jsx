import React, {useState, useEffect} from 'react'
import { Box, Tabs, Tab, Divider, Container, Typography } from '@mui/material'
import { useAlert } from '../../components/common/Alerts/AlertContext';
import UserStoryJobTable from '../../components/common/Jobs/UserStoryJobTable';
import { UserStoryJobContextProvider } from '../../components/common/Jobs/UserStoryJobContextProvider';
import UserStoryJobHandler from '../../utils/JobHandling/UserStoryJobHandler';
import UserStoryJobParametersVisualizer from '../../components/common/Jobs/UserStoryJobParametersVisualizer';
import CompletedJobTable from '../../components/common/Diagrams/CompletedJobTable';

const AnalyzePage = () => {
    const { showAlert } = useAlert();
    const [jobParameters, setJobParameters] = useState("")

    const [tabValue, setTabValue] = useState(0); // Tab Value

    const handleTabChange = (event, newValue) => {
        setTabValue(newValue);
    };

    useEffect(() => {
        // Reconciles status differences between frontend and backend
        const handler = new UserStoryJobHandler();
        handler.syncJobsWithServer().then(response => {
            if (!response.success) {
                showAlert('error', response.message);
            }
        });
    }, []);

    const handleViewUserStoryJobParameters = async (jobId) => {
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.retrieveJobFromQueue(jobId);
            setJobParameters(result.data)
            setTabValue(1);
        }
        catch (error) {
            console.error("Failed to retrieve job parameters", error);
            showAlert('error', 'Failed to retrieve job parameters please try again later.')
        }
    }

    // Function is invoked when a user story job is submitted
    const handleSubmitUserStoryJob = async (jobId) => {
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.submitJob(jobId);
            if (result.success) {
                showAlert("success", `Successfully submitted job: ${jobId}`);
            }
            else {
                showAlert("error", `Failed to submit job: ${jobId}`);
            }
        }
        catch (error) {
            showAlert("error", "Failed to submit your job parameters.");
        }
    }
    // Function is invoked when a user story job is deleted
    const handleDeleteUserStoryJob = async (jobId) => {
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.removeJobFromQueue(jobId);
            if (result.success) {
                showAlert("success", `Successfully removed job: ${jobId} from queue`);
            }
        }
        catch (error) {
            console.error("Error encountered while retrieving job parameters:", error);
            showAlert("error", "Failed to retrieve your job parameters, please try again later.");
        }
    }

    const handleAbortUserStoryJob = async (jobId) => {
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.abortJob(jobId);
            if (result.success) {
                showAlert("success", `Successfully aborted job: ${jobId}`);
            }
            else {
                showAlert("error", `Failed to abort job: ${jobId}, only jobs in Processing state can be aborted`)
            }
        }
        catch (error) {
            console.error("Error encountered while aborting job", error);
            showAlert("error", "Failed to abort job, please try again later.")
        }
    }

    // Function is invoked when user story job is added
    const handleAddUserStoryJob = (job) => {
        console.log(job);
    }

    const handleEditUserStoryJob = async (fileId, recordId, editedData) => {
        const jobId = fileId;  // fileId Here refers to jobId, named as filedId for legacy purposes
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.updateUserStoryInJob(jobId, recordId.feature, recordId.subFeature, recordId.recordId, editedData);
            console.debug("Updated ", result.data);
            if (result.success) {
                setJobParameters(result.data)
                showAlert("success", `Successfully edited user story in job: ${jobId}`);
            }
            else {
                showAlert("error", `Failed to edit user story in job: ${jobId}`)
            }
        }
        catch (error) {
            console.error("Error encountered editing user story in job parameters", error);
            showAlert("error", "Failed to edit user story in job parameters, please try again later.")
        }
    }

    const handleRemoveUserStoryFromJob = async (fileId, recordId) => {
        console.log(fileId, recordId);
        const jobId = fileId; 
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.deleteUserStoryInJob(jobId, recordId.feature, recordId.subFeature, recordId.recordId);
            if (result.success) {
                setJobParameters(result.data)
                showAlert("success", `Successfully deleted user story in job: ${jobId}`);
            }
            else {
                showAlert("error", `Failed to delete user story in job: ${jobId}`)
            }
        }
        catch (error) {
            console.error("Error encountered deleting user story in job parameters", error);
            showAlert("error", "Failed to delete user story in job parameters, please try again later.")
        }
    }
    

    const handleAddUserStoryToJob = async (fileId, newUserStory) => {
        // fileId Here refers to jobId, named as filedId for legacy purposes
        // Adds newUserStory to jobParameters.parameters.job_parameters
        const jobId = fileId;  // fileId Here refers to jobId, named as filedId for legacy purposes
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.updateUserStoryInJob(jobId, newUserStory.feature, newUserStory.sub_feature, newUserStory.id, newUserStory);
            console.debug("Added job parameter ", result.data);
            if (result.success) {
                setJobParameters(result.data)
                showAlert("success", `Successfully edited user story in job: ${jobId}`);
            }
            else {
                showAlert("error", `Failed to edit user story in job: ${jobId}`)
            }
        }
        catch (error) {
            console.error("Error encountered while adding user story to job parameters", error);
            showAlert("error", "Failed to add new user story to job parameters, please try again later.")
        }
    }

    return (
        <UserStoryJobContextProvider
            handleDeleteUserStoryJob={handleDeleteUserStoryJob}
            handleSubmitUserStoryJob={handleSubmitUserStoryJob}
            handleAddUserStoryJob={handleAddUserStoryJob}
            handleViewUserStoryJobParameters={handleViewUserStoryJobParameters}
            handleAbortUserStoryJob={handleAbortUserStoryJob}
            handleEditUserStoryJob={handleEditUserStoryJob}
            handleRemoveUserStoryFromJob={handleRemoveUserStoryFromJob}
            handleAddUserStoryToJob={handleAddUserStoryToJob}
        >   
            <Container>
            <Typography variant='h4'>Analyze and View Results</Typography>
            <Divider sx={{ my: 2 }} /> 
                <Box >
                    <Tabs value={tabValue} onChange={handleTabChange} aria-label="User Story Job Queue Tabs">
                        <Tab label="Job Queue" />
                        <Tab label="Job Parameters" />
                        <Tab label="Completed Jobs" />
                    </Tabs>
                    <Divider sx={{ my: 1 }} /> 
                </Box>
                {tabValue === 0 && (
                    <Box>
                    <Divider sx={{ my: 1 }} />
                    <UserStoryJobTable></UserStoryJobTable>
                    </Box>
                )}
                {tabValue === 1 && (
                    <Box>
                       <UserStoryJobParametersVisualizer
                        jobParameters={jobParameters}
                       ></UserStoryJobParametersVisualizer>
                    </Box>
                )}
                {tabValue === 2 && (
                    <Box>
                        <Typography>View Completed Jobs</Typography>
                        <CompletedJobTable></CompletedJobTable>
                    </Box>
                )}
            </Container>
        </UserStoryJobContextProvider>
    )
}
export default AnalyzePage