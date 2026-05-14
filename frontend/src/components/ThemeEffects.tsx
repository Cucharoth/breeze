'use client';

import { useTheme } from "./ThemeContext";

export function ThemeEffects() {
  const { theme } = useTheme();

  return (
    <>
      {/* Campfire Effects - Toned down as requested */}
      {theme === 'campfire' && (
        <>
          <div className="fixed bottom-[-150px] left-1/2 -translate-x-1/2 w-full h-[300px] bg-orange-600/15 blur-[120px] rounded-full pointer-events-none animate-pulse" />
          <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
            {[...Array(10)].map((_, i) => (
              <div 
                key={i}
                className="absolute bg-orange-500 rounded-full blur-[1px] animate-fire-ember"
                style={{
                  width: Math.random() * 2 + 1 + 'px',
                  height: Math.random() * 2 + 1 + 'px',
                  left: Math.random() * 100 + '%',
                  bottom: '-20px',
                  animationDuration: Math.random() * 4 + 5 + 's',
                  animationDelay: Math.random() * 5 + 's',
                  opacity: Math.random() * 0.2 + 0.1
                }}
              />
            ))}
          </div>
        </>
      )}

      {/* Emerald/Glass Blobs */}
      {(theme === 'glass' || theme === 'emerald') && (
        <div className="fixed w-[600px] h-[600px] z-[-1] top-[-200px] right-[-200px] pointer-events-none bg-primary/10 blur-[100px] rounded-full" />
      )}

      {/* Obsidian Manuscript Effects */}
      {theme === 'obsidian' && (
        <>
          <div className="fixed inset-0 opacity-[0.2] pointer-events-none z-0" 
               style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/black-linen.png")' }} />
          <div className="fixed top-[10%] left-[10%] w-[500px] h-[500px] bg-amber-900/10 blur-[150px] rounded-full pointer-events-none z-0" />
          <div className="fixed bottom-[10%] right-[10%] w-[400px] h-[400px] bg-zinc-900/20 blur-[120px] rounded-full pointer-events-none z-0" />
        </>
      )}
    </>
  );
}
