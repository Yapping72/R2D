import React, { createContext, useContext } from 'react';

// Creating a context for Mermaid-related functionalities.
const MermaidContext = createContext();

/**
 * Custom hook to access Mermaid context.
 * This hook provides a simplified way to access functions related to handling Mermaid files,
 * including uploading and selecting files.
 * @returns {Object} Returns an object containing functions handleFileUpload() and handleFileSelection().
 */
export const useMermaidContext = () => useContext(MermaidContext);

/**
 * Context Provider for Mermaid-related functionalities.
 * Encapsulates functionalities for uploading and selecting Mermaid files.
 * This provider can be extended to include more functions related to Mermaid files by adding more keys to the value object.
 * 
 * @param {Object} props - React component props.
 * @param {Function} props.handleFileUpload - Function to handle the uploading of Mermaid files.
 * @param {Function} props.handleFileSelection - Function to handle the selection of Mermaid files.
 * @param {React.ReactNode} props.children - Child components that will consume the context.
 */
export const MermaidContextProvider = ({ children, handleFileUpload, handleFileSelection }) => (
    <MermaidContext.Provider value={{ handleFileUpload, handleFileSelection }}>
        {children}
    </MermaidContext.Provider>
);
