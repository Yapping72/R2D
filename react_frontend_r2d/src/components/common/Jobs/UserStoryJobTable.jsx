import React from 'react';
import { UserStoryJobQueueRepository } from '../../../utils/Repository/UserStoryJobQueueRepository'
import {Button, Stack, Box, Divider } from '@mui/material'
import GenericJobTable from '../Tables/GenericJobTable';
import UserStoryJobQueueButtons from './UserStoryJobQueueButtons';
import JobStatusChipStack from '../Chips/JobStatusChipStack';
import AddBoxOutlinedIcon from '@mui/icons-material/AddBoxOutlined';

const UserStoryJobTable = () => {
    return (
        <>
        <Box>
        <Stack direction="row">
            <JobStatusChipStack repository={new UserStoryJobQueueRepository()}></JobStatusChipStack>
         </Stack>
        </Box>
        <Box>
            <GenericJobTable
                repository={new UserStoryJobQueueRepository()}
                buttonGroup={<UserStoryJobQueueButtons></UserStoryJobQueueButtons>}>
            </GenericJobTable>
            <Divider sx={{ my: 1 }}></Divider>
        </Box>
        </>
    )
}
export default UserStoryJobTable