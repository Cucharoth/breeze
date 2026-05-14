'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';

export type Theme = 'obsidian' | 'glass' | 'tavern' | 'campfire' | 'emerald';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('obsidian');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Version control for local storage to prevent stale data
    const THEME_VERSION = '1.1'; // Bumped version for Obsidian default
    const savedVersion = localStorage.getItem('breeze-theme-version');
    
    if (savedVersion !== THEME_VERSION) {
      localStorage.removeItem('breeze-theme');
      localStorage.setItem('breeze-theme-version', THEME_VERSION);
    }

    const savedTheme = localStorage.getItem('breeze-theme') as Theme;
    if (savedTheme) {
      setTheme(savedTheme);
      document.body.setAttribute('data-theme', savedTheme);
    } else {
      document.body.setAttribute('data-theme', 'obsidian');
    }
    setMounted(true);
  }, []);

  const handleSetTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    localStorage.setItem('breeze-theme', newTheme);
    document.body.setAttribute('data-theme', newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme: handleSetTheme }}>
      <div style={{ visibility: mounted ? 'visible' : 'hidden' }}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
