import React, { useState, useEffect } from 'react';
import AppTheme from './styles/AppTheme';
import { LanguageProvider } from './contexts';
import { CssBaseline, Box } from '@mui/material';
import { Dashboard } from './layouts';
import { useTerms, useLanguage } from './contexts';
import { getLayoutTranslations } from './translations/layout'
import { initGA, trackPageview } from './utils/analytics';

/**
 * Main Application Component that handles authentication.
 *
 * Responsibilities:
 * - Initializes global app settings (language, analytics, title).
 * - Renders `Dashboard` for authenticated users and `SignIn` for unauthenticated ones.
 * - Bypasses authentication entirely in demo mode.
 * - Updates `dfo-auth-status` in localStorage for external login tracking.
 */
function AppContent() {
  const { language } = useLanguage();
  const appTranslations = getLayoutTranslations('app', language);
  
  // Initialize Google Analytics once on mount
  useEffect(() => {
    initGA();
    trackPageview(window.location.pathname + window.location.search);
  }, []);
  
  // Set HTML lang attribute
  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]); 
  
  // Set document title
  useEffect(() => {
    document.title = appTranslations.title;
  }, [language, appTranslations]);

  return(
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        overflowX: 'hidden',
        bgcolor: 'background.default',
        overflowY: 'auto'
      }}
    >
      <Dashboard  />
    </Box>
  )
}

/**
 * Main Application Component with all providers
 */
function App() {
  return (
    <LanguageProvider>
      <AppTheme>
        <CssBaseline />
          <AppContent />
      </AppTheme>
    </LanguageProvider>
  );
}

export default App;