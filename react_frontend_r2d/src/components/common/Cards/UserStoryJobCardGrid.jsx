import React from 'react';
import UserStoryCard from './UserStoryCard';
import { Container } from '@mui/material';
import { useUserStoryJobContext } from '../Jobs/UserStoryJobContextProvider';
import { Grid, Badge, Chip, Tooltip } from '@mui/material';

/**
 * UserStoryJobCardGrid renders a grid of UserStoryCards for each user story in each sub-feature of each feature.
 * @param {Object} jobParameters - JobParameter dictionary stored in IndexedDB
 * @returns {JSX.Element} A responsive grid layout of user story cards.
 */

const UserStoryJobCardGrid = ({ jobParameters }) => {
  // Helper function to render cards for each user story in a sub-feature
  const { handleEditUserStoryJob, handleRemoveUserStoryFromJob } = useUserStoryJobContext();

  const renderUserStoryCards = (featureName, subFeatureName, subFeatureData) => {
    return Object.entries(subFeatureData).map(([userStoryId, userStoryDetails]) => (
      <Grid key={userStoryId} item xs={12} sm={6} md={4} lg={3}>
        <UserStoryCard
          feature={featureName}
          subFeature={subFeatureName}
          id={userStoryDetails.id}
          requirement={userStoryDetails.requirement}
          recordId={{ // Serves as an identifier to the card
            feature: featureName,
            subFeature: subFeatureName,
            recordId: userStoryDetails.id
          }}
          servicesToUse={userStoryDetails.services_to_use}
          fileId={jobParameters.job_id}
          acceptanceCriteria={userStoryDetails.acceptance_criteria}
          additionalInformation={userStoryDetails.additional_information}
          handleRequirementsEdit={handleEditUserStoryJob}  // Edits the user story parameters in job
          handleRequirementsDelete={handleRemoveUserStoryFromJob}   // Removes the user story job parameter
        />
      </Grid>
    ));
  };

  return (
    <Container>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={11}>
          <Grid container direction="column">
            <Tooltip title="Features" placement="left-start" arrow>
              <Grid item>
                {Array.from(jobParameters.parameters.features).map((feature, index) => (
                  <Chip
                    label={feature} size="small" style={{ marginRight: '5px', marginBottom:'10px' }}
                    variant="outlined" color="primary"
                  />
                ))}
              </Grid>
            </Tooltip>
            <Tooltip title="Sub Features" placement="left-end" arrow>
              <Grid item>
                {Array.from(jobParameters.parameters.sub_features).map((sub_feature, index) => (
                  <Chip
                    label={sub_feature} size="small" style={{ marginRight: '5px', marginBottom:'20px'}}
                    variant="outlined" color="secondary"
                  />
                ))}
              </Grid>
            </Tooltip>
          </Grid>
        </Grid>
      </Grid>
      <Grid container spacing={2}>
        {Object.entries(jobParameters.parameters.job_parameters).map(([featureName, subFeatures]) => (
          Object.entries(subFeatures).map(([subFeatureName, userStories]) => (
            renderUserStoryCards(featureName, subFeatureName, userStories)
          ))
        ))}
      </Grid>
    </Container>
  );
};

export default UserStoryJobCardGrid;
