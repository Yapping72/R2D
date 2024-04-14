import React from 'react';
import Grid from '@mui/material/Grid';
import RequirementsCard from './RequirementsCard';
import { Container } from '@mui/material';
import { useRequirementsContext } from '../Requirements/RequirementsContextProvider';
import AddRequirementCard from './AddRequirementsCard';

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

const RequirementsCardGrid = ({ featureData, fileId}) => {
  const { handleRequirementsEdit } = useRequirementsContext();
  const { handleRequirementsAdd} = useRequirementsContext();

  return (
    <Container>
      <Grid container spacing={2}>
        {featureData.map((item, index) => (
          <Grid item key={index} xs={12} sm={6} md={4} lg={3}>
            <RequirementsCard
              feature={item.feature}
              subFeature={item.sub_feature} 
              id={item.id} 
              requirement={item.requirement}
              recordId = {item.record_identifier}
              services_to_use={Array.isArray(item.services_to_use) ? item.services_to_use : item.services_to_use ? [item.services_to_use] : []}
              fileId={fileId}
              handleRequirementsEdit={handleRequirementsEdit}
            />
          </Grid>
        ))}
        {fileId && (
          <Grid item xs={12} sm={6} md={4} lg={3}>
            <AddRequirementCard 
            fileId={fileId}
            handleRequirementsAdd={handleRequirementsAdd} />
          </Grid>
        )}
      </Grid>
    </Container>
  );
}

export default RequirementsCardGrid;
