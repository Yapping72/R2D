import React, { useState } from 'react';
import { Grid, Box, Typography, Container } from "@mui/material";
import MermaidRenderer from '../../components/common/Mermaid/MermaidRenderer';
import MermaidEditor from '../../components/common/Mermaid/MermaidEditor';
import ZoomAndPan from '../../components/ui/Interactions/ZoomAndPan';
import MermaidTemplatesAccordion from '../../components/common/Mermaid/MermaidTemplatesAccordion';
import MermaidFileManagementAccordion from '../../components/common/Mermaid/MermaidFileManagementAccordion';
import { AlertProvider } from '../../components/common/Alerts/AlertContext';
import './VisualizePage.css'

const VisualizePage = () => {
    const [mermaidCode, setMermaidCode] = useState('');
    const [selectedExample, setSelectedExample] = useState('');

    const handleExampleSelect = (content) => {
      setSelectedExample(content); 
      setMermaidCode(selectedExample);
    };
    const handleDiagramChange = (code) => {
        setMermaidCode(code);
    };

    return (
      <Container>
      <AlertProvider>
      <Typography variant='h3'> Mermaid Editor</Typography>
      <hr></hr> 
      <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, overflow: 'auto'}}>
      <Grid container spacing={2}>
        <Grid item xs={12} md={5} lg={5}> {/* Adjusted for 40% width at large screens */}
        <Box  sx={{ height: '50vh', width:'100%'}}>
                <MermaidEditor mermaidCode={mermaidCode} onCodeChange={handleDiagramChange} />
        </Box>
        <Box>
        <hr></hr>
        <MermaidTemplatesAccordion onExampleSelect={handleExampleSelect}></MermaidTemplatesAccordion>
        <hr></hr>
        <MermaidFileManagementAccordion></MermaidFileManagementAccordion>
        </Box>
        </Grid>
        <Grid item xs={12} md={7} lg={7}> {/* Adjusted for 60% width at large screens */}
        <Box className='drawioGrid' sx={{ height: '100%', width: '100%' }}> {/* Width 100% to fill grid item */}
            <ZoomAndPan >
              <MermaidRenderer chart={mermaidCode}/>
            </ZoomAndPan>
            </Box>
        </Grid>
      </Grid>
    </Box>
    </AlertProvider>
    </Container>
    );
};

export default VisualizePage;
