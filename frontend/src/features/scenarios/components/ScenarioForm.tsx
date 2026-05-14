'use client';

import { useState } from 'react';
import { ThemeIcon } from '@/components/ui/ThemeIcon';
import { useTheme } from '@/components/ThemeContext';

import { useCreateScenario } from '../hooks/useCreateScenario';

export function ScenarioForm() {
  const { theme } = useTheme();
  const [premise, setPremise] = useState('');
  const { createScenario, isLoading } = useCreateScenario();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!premise.trim()) return;
    
    try {
      await createScenario({ premise });
      setPremise('');
      // In the future, the hook will handle the navigation to the story
    } catch (err) {
      // Error is handled by the hook (toast/state)
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <form 
        onSubmit={handleSubmit}
        className="breeze-surface min-h-[500px] flex flex-col"
      >
        <header className="mb-10 flex items-center gap-4 relative z-10">
          <ThemeIcon type="creation" className="text-primary/60" size={24} />
          <h2 className="text-2xl font-bold tracking-tight">
            {theme === 'obsidian' ? "Begin the Chronicle" : "Initialize World"}
          </h2>
          <div className="h-[1px] flex-1 bg-gradient-to-r from-primary/20 to-transparent" />
        </header>

        <div className="flex-1 relative z-10">
          <textarea
            value={premise}
            onChange={(e) => setPremise(e.target.value)}
            placeholder="Describe your world premise..."
            className="breeze-input h-full min-h-[200px] resize-none"
            disabled={isLoading}
          />
        </div>

        <div className="mt-12 flex flex-col items-center gap-8 relative z-10">
          <div className="h-[1px] w-32 bg-gradient-to-r from-transparent via-primary/30 to-transparent" />
          
          <button
            type="submit"
            disabled={isLoading || !premise.trim()}
            className="breeze-btn-primary group"
          >
            <ThemeIcon type="action" size={32} className={isLoading ? "animate-pulse" : ""} />
            
            {/* Semantic Label (Specific to button morphology) */}
            <span className="absolute top-24 left-1/2 -translate-x-1/2 text-[9px] uppercase tracking-[0.5em] font-bold text-primary/50 group-hover:text-primary whitespace-nowrap transition-opacity duration-300">
              {isLoading ? "Igniting..." : "Ignite Reality"}
            </span>
          </button>
        </div>

        {/* Semantic Meta Info */}
        <div className="absolute bottom-6 left-10 right-10 flex justify-between opacity-10 text-[8px] font-mono uppercase tracking-[0.3em] pointer-events-none">
          <span>{theme.toUpperCase()}_#812</span>
          <span>Status: Unsealed</span>
        </div>
      </form>
    </div>
  );
}
