import React, { createContext, useContext } from 'react';

// Creating a context for Requirements-related functionalities.
const UserStoryContext = createContext();

/**
 * Custom hook to access Requirements context.
 * This hook provides a simplified way to access functions related to handling Requirements files,
 * including uploading and selecting files.
 * @returns {Object} Returns an object containing functions handleFileUpload() and handleFileSelection().
 */
export const useUserStoryContext = () => useContext(UserStoryContext);

/**
 * Context Provider for Requirements-related functionalities.
 * Encapsulates functionalities for uploading and selecting Requirements files.
 * This provider can be extended to include more functions related to Requirements files by adding more keys to the value object.
 * 
 * @param {Object} props - React component props.
 * @param {Function} props.handleFileUpload - Function to handle the uploading of Requirements files.
 * @param {Function} props.handleFileSelection - Function to handle the selection of Requirements files.
 * @param {React.ReactNode} props.children - Child components that will consume the context.
 */
export const UserStoryContextProvider = ({ children,
    handleFileUpload,
    handleFileSelection,
    handleRequirementsEdit,
    handleRequirementsAdd,
    handleRequirementsDelete }) => (
    <UserStoryContext.Provider value={{
        handleFileUpload,
        handleFileSelection,
        handleRequirementsAdd,
        handleRequirementsEdit,
        handleRequirementsDelete
    }}>
        {children}
    </UserStoryContext.Provider>
);
