import React from 'react';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import {Container} from "@mui/material";
import IconButton from '@mui/material/IconButton';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import ResetIcon from '@mui/icons-material/Autorenew';

const ZoomAndPan = ({ children }) => {
  return (
    <Container sx={{width: '100%', height: '100%'}}>
    <TransformWrapper
      initialScale={1}
      initialPositionX={0}
      initialPositionY={0}
      limitToBounds={true}
      minScale={0.5}
      maxScale={6}
      centerOnInit={true}
      centerZoomedOut={true}
    >
      {({ zoomIn, zoomOut, resetTransform, ...rest }) => (
        <>
        <div className="tools">
            <IconButton sx={{color:"black"}} onClick={() => zoomIn()} aria-label="zoom in">
              <ZoomInIcon />
            </IconButton>
            <IconButton sx={{color:"black"}} onClick={() => zoomOut()} aria-label="zoom out">
              <ZoomOutIcon />
            </IconButton>
            <IconButton sx={{color:"black"}} onClick={() => resetTransform()} aria-label="reset">
              <ResetIcon />
            </IconButton>
          </div>
          <TransformComponent wrapperStyle={{ width: '100%', height:'90%'}}>
            {children}
          </TransformComponent>
        </>
      )}
    </TransformWrapper>
    </Container>
  );
};

export default ZoomAndPan;
