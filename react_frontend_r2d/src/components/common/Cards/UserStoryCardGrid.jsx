import {React, useState, useEffect} from 'react';
import Grid from '@mui/material/Grid';
import UserStoryCard from './UserStoryCard';
import { Container } from '@mui/material';
import { useUserStoryContext } from '../UserStory/UserStoryContextProvider';
import AddUserStoryCard from './AddUserStoryCard';
import Grow from '@mui/material/Grow';
import { v4 as uuidv4 } from 'uuid';

/**
 * RequirementsCardGrid renders a grid of RequirementCards.
 * It takes feature data and a fileId to handle requirement editing via context.
 * Only shows the AddRequirementCard if a valid fileId is provided.
 * 
 * @param {Object} props Component properties
 * @param {Array} props.featureData Array of objects, each containing details about a feature,
 *                                  expected keys: feature, sub_feature, id, requirement.
 *                                  'services_to_use' is an optional key and should be an array if provided.
 * @param {string} props.fileId Identifier for the file associated with these requirements, used for edit operations.
 * @returns {JSX.Element} A responsive grid layout of requirement cards.
 */

const UserStoryCardGrid = ({featureData, fileId}) => {
  const { handleRequirementsEdit, handleRequirementsAdd, handleRequirementsDelete } = useUserStoryContext();
  const [finishedRendering, setFinishedRendering] = useState(false);

  useEffect(() => {
    // Assuming featureData is loaded all at once and not streamed or paginated
    setFinishedRendering(true);
  }, [featureData]);

  return (
    <Container>
      <Grid container spacing={2}>
        {featureData.map((item, index) => (
          <Grow
            key={item.record_identifier}
            in={true}
            style={{ transformOrigin: '0 0 0' }}
            {...{ timeout: (index + 1) * 500 }} // Stagger the animation
          >
          <Grid item xs={12} sm={6} md={4} lg={3}>
            <UserStoryCard
              feature={item.feature}
              subFeature={item.sub_feature}
              id={item.id}
              requirement={item.requirement}
              recordId={item.record_identifier}
              servicesToUse={Array.isArray(item.services_to_use) ? item.services_to_use : item.services_to_use ? [item.services_to_use] : []}
              fileId={fileId}
              acceptanceCriteria={item.acceptance_criteria}
              additionalInformation={item.additional_information}
              handleRequirementsEdit={handleRequirementsEdit}
              handleRequirementsDelete={handleRequirementsDelete}
            />
          </Grid>
          </Grow>
        ))}
        {fileId && (
          <Grow
            in={finishedRendering} // Only transition in after all the UserStoryCards have rendered
            style={{ transformOrigin: '0 0 0' }}
            {...{ timeout: (featureData.length * 500) + 500 }} // AddUserStoryCard grows after the last UserStoryCard
          >
          <Grid item xs={12} sm={6} md={4} lg={3}>
            <AddUserStoryCard
              fileId={fileId}
              handleRequirementsAdd={handleRequirementsAdd} />
          </Grid>
          </Grow>
        )}
      </Grid>
    </Container>
  );
}

export default UserStoryCardGrid;
