import React from 'react';
import GenericFileTable from '../Tables/GenericFileTable';
import R2DTableModal from '../Modals/R2DTableModal'
import { RequirementsFileRepository } from '../../../utils/Repository/RequirementsFileRepository';
import SearchIcon from '@mui/icons-material/Search';
import { useUserStoryContext } from './UserStoryContextProvider';


const UserStoryTable = () => {
    const { handleFileSelection, _ } = useUserStoryContext();
    return(
        <R2DTableModal title="View User Stories" icon={<SearchIcon></SearchIcon>}>
                <GenericFileTable repository={new RequirementsFileRepository()} handleFileSelection={handleFileSelection}></GenericFileTable>
        </R2DTableModal>
   
    )
}
export default UserStoryTable