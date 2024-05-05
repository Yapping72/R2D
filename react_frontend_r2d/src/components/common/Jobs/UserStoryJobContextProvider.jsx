import React, { createContext, useContext } from 'react';

// Creating a context for user story jobs content
const userStoryJobContext = createContext();

/**
 * Custom hook to access user story jobs context.
 * This hook provides a simplified way to access functions related to handling user story jobs
 * including uploading and selecting files.
 * @returns {Object} Returns an object containing handleDeleteUserStoryJob, handleSubmitUserStoryjob, handleAddUserStoryJob, handleViewUserStoryJobParameters, handleAbortUserStoryJob, handleEditUserStoryJob, handleAddUserStoryToJob
 */
export const useUserStoryJobContext = () => useContext(userStoryJobContext);

/**
 * Context Provider for user story job related functionalities.
 * Encapsulates functionalities for deleting and submitting a user story job
 * This provider can be extended to include more functions related to Requirements files by adding more keys to the value object.
 * 
 * @param {Object} props - React component props.
 * @param {Function} props.handleDeleteUserStoryJob- Function to handle the deletion  of user story jobs, triggers a BE request to delete completed jobs
 * @param {Function} props.handleSubmitUserStoryJob - Function to handle the submission of user story jobs, triggers a BE request to submit job
 * @param {Function} props.handleAddUserStoryJob - Function to add user story job, this adds an entirely new user story job
 * @param {Function} props.handleViewUserStoryJobParameters - Function to retrieve user story job parameters
 * @param {Function} props.handleAbortUserStoryJob - Handle aborting jobs that are currently in the JobStatus.PROCESSING status
 * @param {Function} props.handleEditUserStoryJob - Modify an existing UserStoryJob parameter
 * @param {Function} props.handleRemoveUserStoryFromJob - Removes ONE user story from job parameters
 * @param {Function} props.handleAddUserStoryToJob - Adds ONE user story to job parameters
 * @param {React.ReactNode} props.children - Child components that will consume the context.
 */
export const UserStoryJobContextProvider = ({ children,
    handleDeleteUserStoryJob,
    handleSubmitUserStoryJob,
    handleAddUserStoryJob,
    handleViewUserStoryJobParameters,
    handleAbortUserStoryJob,
    handleEditUserStoryJob,
    handleRemoveUserStoryFromJob,
    handleAddUserStoryToJob
}) => (
    <userStoryJobContext.Provider value={{
        handleDeleteUserStoryJob,
        handleSubmitUserStoryJob,
        handleAddUserStoryJob,
        handleViewUserStoryJobParameters,
        handleAbortUserStoryJob,
        handleEditUserStoryJob,
        handleRemoveUserStoryFromJob,
        handleAddUserStoryToJob
    }}>
        {children}
    </userStoryJobContext.Provider>
);
