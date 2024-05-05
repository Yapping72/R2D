import React from 'react';
import { UserStoryJobQueueRepository } from '../../../utils/Repository/UserStoryJobQueueRepository'
import { Box, Divider } from '@mui/material'
import ClearIndexedDbButton from '../../ui/Button/ClearIndexedDbButton'
import GenericJobTable from '../Tables/GenericJobTable';
import UserStoryJobQueueButtons from './UserStoryJobQueueButtons';


const UserStoryJobTable = () => {
    return (
        <Box>
            <GenericJobTable
                repository={new UserStoryJobQueueRepository()}
                buttonGroup={<UserStoryJobQueueButtons></UserStoryJobQueueButtons>}>
            </GenericJobTable>
            <Divider sx={{ my: 1 }}></Divider>
            <ClearIndexedDbButton repository={new UserStoryJobQueueRepository()}></ClearIndexedDbButton>
        </Box>
    )
}
export default UserStoryJobTable