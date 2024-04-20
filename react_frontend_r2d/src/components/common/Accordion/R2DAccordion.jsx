import React, { useState } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography  } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';


const R2DAccordion = ({ title, children, defaultExpanded=false, icon = ""}) => {
  const [expanded, setExpanded] = useState(defaultExpanded);

  const handleExpansion = () => {
    setExpanded(!expanded);
  };

  return (
    <Accordion 
    onChange={handleExpansion} 
    expanded={expanded}
    >
      <AccordionSummary
        expandIcon={<ExpandMoreIcon />}
        aria-controls="panel-content"
        id="panel-header"
      >
        {/* Render the icon if provided */}
        {icon && <span style={{ marginRight: 8 }}>{icon}</span>}
        <Typography>{title}</Typography>
      </AccordionSummary>
      <AccordionDetails>
        {children}
      </AccordionDetails>
    </Accordion>
  );
};

export default R2DAccordion;
