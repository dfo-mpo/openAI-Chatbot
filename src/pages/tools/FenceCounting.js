/**
 * Fence Counting Tool Component
 * 
 * Main component for the Fence Counting tool, which uses computer vision to count
 * fish in monitoring videos. This component displays the user interface for the tool,
 * including its description, video upload functionality, and sample video options.
 */

import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Button,
  Paper,
  Grid,
} from '@mui/material';
import { Play, Upload } from 'lucide-react'; 
import { ToolPage } from '../../components/tools';
import { getToolTranslations } from '../../utils';
import { useComponentStyles } from '../../styles/hooks/useComponentStyles';
import { processFenceCounting } from '../../services/apiService';
import { useLanguage, useToolSettings } from '../../contexts';
import { trackEvent } from '../../utils/analytics';
import { useIsAuthenticated } from '@azure/msal-react';

export function FenceCounting() {
  const { language } = useLanguage();
  const { fenceCountingSettings } = useToolSettings();
  const toolData = getToolTranslations("fenceCounting", language);
  const toolStyles = useComponentStyles('tool');
  const isAuth = useIsAuthenticated();

  return (
    <ToolPage
      title={toolData.title}
      shortDescription={toolData.shortDescription}
      longDescription={toolData.longDescription}
      backgroundImage="/assets/fence-counting.png"
      hideActionButton={true}
      containerSx={toolStyles.container}
    >
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
              src={(language === 'fr')? 'https://fence-counting-demo.azurewebsites.net/fr' : 'https://fence-counting-demo.azurewebsites.net/'}
              sx={{
                position: 'absolute',
                top: '-60px',
                left: 0,
                width: '100%',
                height: 'calc(100vh + 120px)',
              }}
            />
          </Box>
    </ToolPage>
  );
}

export default FenceCounting;