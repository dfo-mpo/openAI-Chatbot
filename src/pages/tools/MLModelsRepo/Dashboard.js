/**
 * ML Model Repository Dashboard
 */

import React from 'react';
import { Box } from '@mui/material';

export function MLModelsRepo() {
  return (
    <Box 
      sx={{
        position: 'relative',
        width: '100%',
        height: '100vh',
        overflow: 'hidden'
      }}
    >
      <Box
        component='iframe'
        src='https://ml-model-repo-demo.azurewebsites.net/'
        sx={{
          position: 'absolute',
          left: 0,
          width: '100%',
          height: 'calc(100vh)',
        }}
      />
    </Box>
        // <iframe src="https://ocds-ai-portal.canadacentral.cloudapp.azure.com/ocds-ctd/" sandbox="allow-scripts allow-same-origin" width="100%" frameborder="0" style={{marginTop: '-120px', height: '100vh'}}></iframe>  
  );
}

export default MLModelsRepo;