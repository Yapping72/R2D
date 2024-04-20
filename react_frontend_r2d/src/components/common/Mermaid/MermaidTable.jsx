import React from 'react';
import GenericFileTable from '../Tables/GenericFileTable';
import {MermaidFileRepository} from '../../../utils/Repository/MermaidFileRepository';
import SearchIcon from '@mui/icons-material/Search';
import R2DTableModal from '../Modals/R2DTableModal';

const MermaidTable = ({handleFileSelection}) => {
    return(
        <R2DTableModal title="View Uploaded Files" icon={<SearchIcon></SearchIcon>} sx={{width:"100vw"}}>
        <GenericFileTable repository={new MermaidFileRepository()} handleFileSelection={handleFileSelection}></GenericFileTable>
        </R2DTableModal>
    )
}
export default MermaidTable