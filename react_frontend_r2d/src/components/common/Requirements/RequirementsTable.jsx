import React from 'react';
import GenericFileTable from '../Tables/GenericFileTable';
import R2DTableModal from '../Modals/R2DTableModal'
import { RequirementsFileRepository } from '../../../utils/Repository/RequirementsFileRepository';
import SearchIcon from '@mui/icons-material/Search';
import { useRequirementsContext } from './RequirementsContextProvider';


const RequirementsTable = () => {
    const { handleFileSelection, _ } = useRequirementsContext();
    return(
        <R2DTableModal title="View Uploaded Requirements" icon={<SearchIcon></SearchIcon>}>
                <GenericFileTable repository={new RequirementsFileRepository()} handleFileSelection={handleFileSelection}></GenericFileTable>
        </R2DTableModal>
   
    )
}
export default RequirementsTable