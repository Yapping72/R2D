import React from 'react';

import {UserStoryJobQueueRepository} from '../../../utils/Repository/UserStoryJobQueueRepository'
import {Box, Divider, Button} from '@mui/material'
import ClearIndexedDbButton from '../../ui/Button/ClearIndexedDbButton'
import GenericJobTable from '../Tables/GenericJobTable';
import JobButtons from './JobButtons';

const UserStoryJobTable = () => {
    return(
        <Box>
        <GenericJobTable repository={new UserStoryJobQueueRepository()} buttonGroup={<JobButtons></JobButtons>}></GenericJobTable>
        <Divider sx={{my:1}}></Divider>
        <ClearIndexedDbButton repository={new UserStoryJobQueueRepository()}></ClearIndexedDbButton>
        <JobButtons></JobButtons>
        </Box>

    )
}
export default UserStoryJobTable