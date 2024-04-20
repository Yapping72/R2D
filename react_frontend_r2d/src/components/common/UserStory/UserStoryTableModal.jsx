import React from 'react';
import GenericFileTable from '../Tables/GenericFileTable';
import { UserStoryFileRepository } from '../../../utils/Repository/UserStoryFileRepository';
import SearchIcon from '@mui/icons-material/Search';
import { useUserStoryContext } from './UserStoryContextProvider';
import R2DTableModal from '../Modals/R2DTableModal';

const UserStoryTableModal = () => {
    const { handleFileSelection, _ } = useUserStoryContext();
    return(
        <R2DTableModal title="View Uploaded Files" icon={<SearchIcon></SearchIcon>} sx={{width:"100vw"}}>
        <GenericFileTable repository={new UserStoryFileRepository()} handleFileSelection={handleFileSelection}></GenericFileTable>
        </R2DTableModal>
    )
}
export default UserStoryTableModal