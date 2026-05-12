/**
 * Dashboard Layout Component
 * 
 * Main layout component for the DFO AI Portal. Manages the overall page structure 
 * including the header, left panel (for tool selection), and dynamic content area
 * that loads different tools based on user selection.
 */

import React, { useState, Suspense, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useTheme, useMediaQuery, Box, Paper, CircularProgress, Alert, IconButton } from '@mui/material';
import { getToolByName, getParam, getAllParams, updateURLParams } from '../utils';
import { trackEvent } from '../utils/analytics';
import { MLModelsRepo } from '../pages';
import { useLanguage, } from '../contexts';
import { Footer, TermsModalContainer } from '../components/common';
import { getLayoutTranslations } from '../translations/layout'
import { useComponentStyles } from '../styles/hooks/useComponentStyles';

export default function Dashboard() {
  // Store the selected tool name
  const [selectedTool, setSelectedTool] = useState('');
  const [headerHeight, setHeaderHeight] = useState(80); // Default to 80px, dynamically updated
  const { language } = useLanguage();
  const dashboardTranslations = getLayoutTranslations('dashboard', language);

  // Use the styling hook with the dashboard style collection
  const styles = useComponentStyles('dashboard', { headerHeight });

  // Retrieve all current URL search parameters once on load
  const searchParams = getAllParams();
  
  useEffect(()=>{
    // If param detected on load, switch to tool page
    if (getParam('view')) {
      const view = getParam('view');
      console.log(view)
      // Try to match param to a known tool
      const tool = getToolByName(view);
      if (view && tool) {
        // If the tool is valid, update the selected tool in state
        setSelectedTool(view);
      } else {
        // If param is invalid or unrecognized, clean the URL
        updateURLParams({});
      }
    }
  }, [searchParams]);

  return (
    // <Box sx={styles.dashboardWrapper}>
    //   {/* Main content area */}
      // <Box 
      //   sx={{
      //     ...styles.mainWrapper,
      //   }}
      // >
        // {/* Content wrapper with improved responsive layout and spacing */}
        // <Box sx={styles.contentWrapper}>
        //   {/* Main content area with improved overflow handling */}
        //   <Box sx={styles.mainContent}>
        //     {/* Tool content with proper overflow handling */}
        //     <Paper sx={styles.contentPaper}>
        //       <Suspense
        //         fallback={
        //           <Box sx={styles.loadingContainer}>
        //             <CircularProgress />
        //           </Box>
        //         }
        //       >
                <MLModelsRepo/>
        //       </Suspense>
        //     </Paper>
        //   </Box>
        // </Box>
      // </Box>
    // </Box>
  );
}