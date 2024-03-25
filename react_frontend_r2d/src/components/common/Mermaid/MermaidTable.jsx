import React from 'react';
import GenericFileTable from '../Tables/GenericFileTable';
import {MermaidFileRepository} from '../../../utils/Repository/MermaidFileRepository';
import R2DModal from '../Modals/R2DModal'
import { Typography } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const MermaidTable = () => {
    return(
        <R2DModal title=<><SearchIcon></SearchIcon>View Uploaded Files</>>
        <GenericFileTable repository={new MermaidFileRepository()}></GenericFileTable>
        </R2DModal>
    )
}
export default MermaidTable