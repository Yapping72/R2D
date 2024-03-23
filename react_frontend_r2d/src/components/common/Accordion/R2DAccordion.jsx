import React, { useState } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const R2DAccordion = ({ title, children, defaultExpanded = false, ...otherProps }) => {
  const [expanded, setExpanded] = useState(defaultExpanded);

  const handleExpansion = (event, isExpanded) => {
    setExpanded(isExpanded);
  };

  return (
    <Accordion 
    expanded={expanded} 
    onChange={handleExpansion} 
    {...otherProps}
    >
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel-content"
        id="panel-header"
      >
        <Typography>{title}</Typography>
      </AccordionSummary>
      <AccordionDetails>
        {children}
      </AccordionDetails>
    </Accordion>
  );
};

export default R2DAccordion;
