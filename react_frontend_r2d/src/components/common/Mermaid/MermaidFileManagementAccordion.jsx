import {React} from 'react';
import { Box } from '@mui/material';

import DragDropFileUpload from '../FileUpload/DragDropFileUpload';
import R2DAccordion from '../Accordion/R2DAccordion';
import FileUploadValidator from '../../../utils/Validators/FileUploadValidator';
import {MermaidFileRepository} from '../../../utils/Repository/MermaidFileRepository';
import MermaidTable from './MermaidTable'
import ClearIndexedDbButton from '../../ui/Button/ClearIndexedDbButton';
import { useMermaidContext } from '../Mermaid/MermaidContextProvider';

const MermaidFileManagementAccordion = () => {
    const { handleFileSelection, handleFileUpload } = useMermaidContext();
    return (
        <R2DAccordion title="Upload Your Diagrams Here">
             <DragDropFileUpload 
             validator={new FileUploadValidator(['txt', 'mmd','md'])} 
             repository={new MermaidFileRepository()}
             handleFileUpload={handleFileUpload}
             ></DragDropFileUpload>
             <p></p>
             <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                <MermaidTable handleFileSelection={handleFileSelection}></MermaidTable>
                <ClearIndexedDbButton repository={new MermaidFileRepository()}></ClearIndexedDbButton>
             </Box>
        </R2DAccordion>
    )
}
export default MermaidFileManagementAccordion