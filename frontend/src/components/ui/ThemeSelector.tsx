'use client';

import { useTheme, Theme } from '@/components/ThemeContext';
import { Palette, ChevronDown } from 'lucide-react';
import { useState } from 'react';
import { cn } from '@/lib/utils';

const themes: { id: Theme; label: string; icon: string }[] = [
  { id: 'obsidian', label: 'Obsidian Manuscript', icon: '🌑' },
  { id: 'glass', label: 'Glassmorphism', icon: '💎' },
  { id: 'tavern', label: 'Forest Tavern', icon: '🌲' },
  { id: 'campfire', label: 'Campfire', icon: '🔥' },
  { id: 'emerald', label: 'Emerald Mist', icon: '✨' },
];

export function ThemeSelector() {
  const { theme, setTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative inline-block text-left">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm font-medium hover:bg-white/10 transition-all text-text-primary"
      >
        <Palette size={16} className="text-primary" />
        <span className="capitalize">{themes.find(t => t.id === theme)?.label}</span>
        <ChevronDown size={14} className={cn("transition-transform", isOpen && "rotate-180")} />
      </button>

      {isOpen && (
        <>
          <div 
            className="fixed inset-0 z-40" 
            onClick={() => setIsOpen(false)} 
          />
          <div className="absolute right-0 mt-2 w-64 bg-zinc-950 border border-white/10 rounded-2xl shadow-2xl z-50 overflow-hidden animate-fade-in">
            {themes.map((t) => (
              <button
                key={t.id}
                onClick={() => {
                  setTheme(t.id);
                  setIsOpen(false);
                }}
                className={cn(
                  "w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors hover:bg-white/5",
                  theme === t.id ? "text-primary bg-primary/10" : "text-zinc-500"
                )}
              >
                <span className="text-lg">{t.icon}</span>
                <span className="flex-1 text-left font-medium">{t.label}</span>
                {theme === t.id && <div className="w-1.5 h-1.5 rounded-full bg-primary" />}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
