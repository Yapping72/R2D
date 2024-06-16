import React, { useState } from 'react';
import { Grid, Box, Typography, Container, Divider } from "@mui/material";
import MermaidRenderer from '../../components/common/Mermaid/MermaidRenderer';
import MermaidEditor from '../../components/common/Mermaid/MermaidEditor';
import ZoomAndPan from '../../components/ui/Interactions/ZoomAndPan';
import MermaidTemplatesAccordion from '../../components/common/Mermaid/MermaidTemplatesAccordion';
import MermaidFileManagementAccordion from '../../components/common/Mermaid/MermaidFileManagementAccordion';
import { MermaidContextProvider } from '../../components/common/Mermaid/MermaidContextProvider';
import { AlertProvider } from '../../components/common/Alerts/AlertContext';
import { mermaidExamples } from '../../components/common/Mermaid/MermaidTemplatesAccordion';
import FileReaderUtility from '../../utils/FileHandling/FileReaderUtility';
import './VisualizePage.css'
import { useAuth } from '../../components/common/Authentication/AuthContext';

const VisualizePage = () => {
  const { isLoggedIn } = useAuth(); // Get the login status from AuthContext - Display file upload accordion if logged in
  // Randomly select an example from mermaidExamples when initializing state
  const [mermaidCode, setMermaidCode] = useState(() => {
    const randomIndex = Math.floor(Math.random() * mermaidExamples.length);
    return mermaidExamples[randomIndex].content;
  });

  const [selectedExample, setSelectedExample] = useState('');
  // Selects an example and sets it in the MermaidEditor
  const handleExampleSelect = (content) => {
    setSelectedExample(content);
    setMermaidCode(selectedExample);
  };

  // Renders the diagram whenever there is a change in the editor
  const handleDiagramChange = (code) => {
    setMermaidCode(code);
  };

  // Defines the actions to take when a file is uploaded to the MermaidFileManagementAccordion (DragDropComponent)
  const handleFileUpload = async (file, file_metadata) => {
    // Callback function that will read the file 
    const fileContents = await FileReaderUtility.readAsText(file);
    setMermaidCode(fileContents)
  };

  // Defines the actions to take when a file is selected from the mermaid table 
  const handleFileSelection = (fileContents) => {
    setMermaidCode(fileContents)
  };

  return (
    <MermaidContextProvider handleFileUpload={handleFileUpload} handleFileSelection={handleFileSelection}>
      <Container>
        <AlertProvider>
          <Box>
            <Typography variant='h4'> Mermaid Live Editor</Typography>
            <Divider sx={{ my: 2 }}></Divider>
            {isLoggedIn && (
              <>
                <MermaidFileManagementAccordion handleFileUpload={handleFileUpload} handleFileSelection={handleFileSelection} />
                <Divider sx={{ my: 1 }}></Divider>
              </>
            )}            
            <MermaidTemplatesAccordion onExampleSelect={handleExampleSelect}></MermaidTemplatesAccordion>
          </Box>
          <Divider sx={{ my: 2 }}></Divider>
          <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1, overflow: 'hidden' }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={5} lg={5}>
                <Box sx={{ height: '100vh', width: '100%' }}>
                  <MermaidEditor mermaidCode={mermaidCode} onCodeChange={handleDiagramChange} />
                </Box>
              </Grid>
              <Grid item xs={12} md={7} lg={7}>
                <Box className='drawioGrid' sx={{ height: '100vh', width: '100%' }}>
                  <ZoomAndPan >
                    <MermaidRenderer chart={mermaidCode} />
                  </ZoomAndPan>
                </Box>
              </Grid>
            </Grid>
          </Box>
        </AlertProvider>
      </Container>
    </MermaidContextProvider>
  );
};

export default VisualizePage;
