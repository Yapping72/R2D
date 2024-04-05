import {React, useEffect} from 'react';
import DragDropFileUpload from '../FileUpload/DragDropFileUpload';
import R2DAccordion from '../Accordion/R2DAccordion';
import FileUploadValidator from '../../../utils/Validators/FileUploadValidator';
import {MermaidFileRepository} from '../../../utils/Repository/MermaidFileRepository';
import MermaidTable from './MermaidTable'
import ClearIndexedDbButton from '../../ui/Button/ClearIndexedDbButton';
import { Box } from '@mui/material';
import FileReaderUtility from '../../../utils/FileReaders/FileReaderUtility';

const MermaidFileManagementAccordion = ({ handleFileUpload }) => {
    const onFileUpload = async (file) => {
        // Callback function that is passed to DragDropFileUpload component
        // Reads the fileContent and passes it back to the calling Component e.g., VisualizePage
        const fileContent = await FileReaderUtility.readAsText(file);  
        handleFileUpload(fileContent) 
    }

    return (
        <R2DAccordion title="Upload Your Diagrams Here">
             <DragDropFileUpload 
             validator={new FileUploadValidator(['txt', 'mmd','md'])} 
             repository={new MermaidFileRepository()}
             onFileUpload={onFileUpload} 
             ></DragDropFileUpload>
             <p></p>
             <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
             <MermaidTable></MermaidTable>
             <ClearIndexedDbButton repository={new MermaidFileRepository()}></ClearIndexedDbButton>
             </Box>
        </R2DAccordion>
    )
}
export default MermaidFileManagementAccordion