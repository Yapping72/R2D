import React, { createContext, useContext } from 'react';

// Creating a context for user story jobs content
const userStoryJobContext = createContext();

/**
 * Custom hook to access user story jobs context.
 * This hook provides a simplified way to access functions related to handling user story jobs
 * including uploading and selecting files.
 * @returns {Object} Returns an object containing handleDeleteUserStoryJob, handleSubmitUserStoryjob, handleAddUserStoryJob, handleViewUserStoryJobParameters, handleAbortUserStoryJob
 */
export const useUserStoryJobContext = () => useContext(userStoryJobContext);

/**
 * Context Provider for user story job related functionalities.
 * Encapsulates functionalities for deleting and submitting a user story job
 * This provider can be extended to include more functions related to Requirements files by adding more keys to the value object.
 * 
 * @param {Object} props - React component props.
 * @param {Function} props.handleDeleteUserStoryJob- Function to handle the deletion  of user story jobs
 * @param {Function} props.handleSubmitUserStoryJob - Function to handle the submission of user story jobs
 * @param {Function} props.handleAddUserStoryJob - Function to add user story job
 * @param {Function} props.handleViewUserStoryJobParameters - Function to retrieve user story job parameters 
 * @param {React.ReactNode} props.children - Child components that will consume the context.
 */
export const UserStoryJobContextProvider = ({ children,
    handleDeleteUserStoryJob,
    handleSubmitUserStoryJob,
    handleAddUserStoryJob,
    handleViewUserStoryJobParameters,
    handleAbortUserStoryJob,
}) => (
    <userStoryJobContext.Provider value={{
        handleDeleteUserStoryJob,
        handleSubmitUserStoryJob,
        handleAddUserStoryJob,
        handleViewUserStoryJobParameters,
        handleAbortUserStoryJob
    }}>
        {children}
    </userStoryJobContext.Provider>
);
