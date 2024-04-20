import React from 'react';
import GenericFileTable from '../Tables/GenericFileTable';
import { UserStoryFileRepository } from '../../../utils/Repository/UserStoryFileRepository';
import SearchIcon from '@mui/icons-material/Search';
import { useUserStoryContext } from './UserStoryContextProvider';
import {Box, Divider} from '@mui/material'
import ClearIndexedDbButton from '../../ui/Button/ClearIndexedDbButton'
const UserStoryTable = () => {
    const { handleFileSelection, _ } = useUserStoryContext();
    return(
        <Box>
        <GenericFileTable repository={new UserStoryFileRepository()} handleFileSelection={handleFileSelection}></GenericFileTable>
        <Divider sx={{my:1}}></Divider>
        <ClearIndexedDbButton repository={new UserStoryFileRepository()}></ClearIndexedDbButton>
        </Box>
    )
}
export default UserStoryTable