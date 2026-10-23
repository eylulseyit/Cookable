import { useEffect, useState } from 'react';

export type Theme = 'light' | 'dark';

const STORAGE_KEY = 'theme';
const systemQuery = window.matchMedia('(prefers-color-scheme: dark)');

function savedTheme(): Theme | null {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    return value === 'light' || value === 'dark' ? value : null;
  } catch {
    return null;
  }
}

function applyTheme(theme: Theme) {
  document.documentElement.classList.toggle('dark', theme === 'dark');
}

/**
 * Light/dark theme. Follows the OS setting until the user picks one with
 * toggle(); the inline script in index.html applies it before first paint.
 */
export function useTheme() {
  const [theme, setTheme] = useState<Theme>(
    () => savedTheme() ?? (systemQuery.matches ? 'dark' : 'light'),
  );

  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  useEffect(() => {
    const onSystemChange = (e: MediaQueryListEvent) => {
      if (!savedTheme()) setTheme(e.matches ? 'dark' : 'light');
    };
    systemQuery.addEventListener('change', onSystemChange);
    return () => systemQuery.removeEventListener('change', onSystemChange);
  }, []);

  const toggle = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      // Storage can be unavailable (e.g. private mode); the theme still switches
    }
    setTheme(next);
  };

  return { theme, toggle };
}
