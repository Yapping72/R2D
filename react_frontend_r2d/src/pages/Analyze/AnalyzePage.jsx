import React from 'react'
import { Container } from '@mui/material'
import { useAlert } from '../../components/common/Alerts/AlertContext';
import UserStoryJobTable from '../../components/common/Jobs/UserStoryJobTable';
import { UserStoryJobContextProvider } from '../../components/common/Jobs/UserStoryJobContextProvider';
import UserStoryJobHandler from '../../utils/JobHandling/UserStoryJobHandler';

const AnalyzePage = () => {
    const { showAlert } = useAlert();
    const handleViewUserStoryJobParameters = async (jobId) => {
        const handler = new UserStoryJobHandler();
        try {
            let result = await handler.retrieveJobFromQueue(jobId);
            console.log(result.data.job_id);
            console.log(result.data.parameters.job_parameters);
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
        console.debug(job);
        // Add job parameters to queue
    }

    return (
        <UserStoryJobContextProvider
            handleDeleteUserStoryJob={handleDeleteUserStoryJob}
            handleSubmitUserStoryJob={handleSubmitUserStoryJob}
            handleAddUserStoryJob={handleAddUserStoryJob}
            handleViewUserStoryJobParameters={handleViewUserStoryJobParameters}
            handleAbortUserStoryJob={handleAbortUserStoryJob}
        >
            <Container>
                <UserStoryJobTable></UserStoryJobTable>
            </Container>
        </UserStoryJobContextProvider>
    )
}
export default AnalyzePage