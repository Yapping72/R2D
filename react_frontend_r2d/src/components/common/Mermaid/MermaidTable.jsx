import React from 'react';
import GenericFileTable from '../Tables/GenericFileTable';
import {MermaidFileRepository} from '../../../utils/Repository/MermaidFileRepository';
import R2DModal from '../Modals/R2DModal'
import SearchIcon from '@mui/icons-material/Search';


const MermaidTable = ({handleFileSelection}) => {
    return(
        <R2DModal title="View Uploaded Files" icon={<SearchIcon></SearchIcon>}>
        <GenericFileTable repository={new MermaidFileRepository()} handleFileSelection={handleFileSelection}></GenericFileTable>
        </R2DModal>
    )
}
export default MermaidTable