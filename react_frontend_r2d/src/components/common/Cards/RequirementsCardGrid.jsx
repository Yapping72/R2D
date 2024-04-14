import React from 'react';
import Grid from '@mui/material/Grid';
import RequirementsCard from './RequirementsCard';
import { Container } from '@mui/material';
import { useRequirementsContext } from '../Requirements/RequirementsContextProvider';


/**
 * featureData is expected to have feature, sub_feature, id, requirement as keys. services_to_use is optional
 * Note that if services_to_use is provided it should be in an array format
 * @param {*} param0 
 * @returns 
 */
const RequirementsCardGrid = ({ featureData, fileId}) => {
  const { handleRequirementsEdit } = useRequirementsContext();

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
      </Grid>
    </Container>
  );
}

export default RequirementsCardGrid;
