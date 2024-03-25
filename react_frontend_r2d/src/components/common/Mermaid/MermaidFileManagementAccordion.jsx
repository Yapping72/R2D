import React from 'react';
import DragDropFileUpload from '../FileUpload/DragDropFileUpload';
import R2DAccordion from '../Accordion/R2DAccordion';
import FileUploadValidator from '../../../utils/Validators/FileUploadValidator';
import {MermaidFileRepository} from '../../../utils/Repository/MermaidFileRepository';
import MermaidTable from './MermaidTable'
import ClearIndexedDbButton from '../../ui/Button/ClearIndexedDbButton';
import { Box } from '@mui/material';

const MermaidFileManagementAccordion = () => {
    return (
        <R2DAccordion title="Upload to Editor">
             <DragDropFileUpload validator={new FileUploadValidator(['txt', 'mmd','md'])} repository={new MermaidFileRepository()}></DragDropFileUpload>
             <p></p>
             <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
             <MermaidTable></MermaidTable>
             <ClearIndexedDbButton repository={new MermaidFileRepository()}></ClearIndexedDbButton>
             </Box>
        </R2DAccordion>
    )
}
export default MermaidFileManagementAccordion