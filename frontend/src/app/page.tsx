'use client';

import { useState } from 'react';
import { Sparkles, Terminal } from 'lucide-react';
import { logger } from '@/lib/logger';
import api from '@/lib/api';
import { ScenarioCreateSchema } from '@/schemas/scenario';

export default function Home() {
  const [premise, setPremise] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Zod validation using the "next-best-practices" pattern (safeParse + infer)
    const result = ScenarioCreateSchema.safeParse({ premise });
    if (!result.success) {
      logger.warn('Validation failed', result.error.errors);
      alert(result.error.errors[0].message);
      return;
    }

    setLoading(true);
    try {
      logger.info('Submitting premise:', premise);
      const response = await api.post('/scenarios/', { premise });
      logger.info('Scenario created:', response.data);
      alert(`Scenario Created! ID: ${response.data.id}\nWorld Lore: ${response.data.world_lore}`);
    } catch (err) {
      logger.error('Failed to create scenario', err);
      alert('Failed to connect to backend. Make sure it is running!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="main-container animate-fade-in">
      <header className="mb-20 text-center">
        <h1 className="text-[4.5rem] font-extrabold tracking-tight">
          Breeze<span className="text-primary">.</span>
        </h1>
        <p className="text-xl opacity-80">
          Crafting parallel timelines with a single breath.
        </p>
      </header>

      <section className="glass-panel mx-auto max-w-[800px]">
        <div className="flex items-center gap-3 mb-6">
          <Sparkles className="size-6 text-primary" />
          <h2 className="m-0 text-2xl font-bold">Start a new World</h2>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block mb-2.5 text-[0.8rem] font-semibold tracking-[0.1em] text-text-secondary uppercase">
              THE PREMISE
            </label>
            <textarea 
              className="input-glass"
              placeholder="e.g., A cyberpunk detective in Neo-Tokyo investigating a ghost in the machine..."
              value={premise}
              onChange={(e) => setPremise(e.target.value)}
              rows={4}
              style={{ resize: 'none' }}
            />
          </div>

          <div className="flex justify-between items-center gap-4">
            <p className="text-sm max-w-[300px] text-text-secondary">
              Your world will be generated using the configured LLM provider.
            </p>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Initializing World...' : (
                <>
                  <Terminal className="size-4" />
                  Generate Scenario
                </>
              )}
            </button>
          </div>
        </form>
      </section>
      
      <footer className="mt-32 text-center text-[0.8rem] text-text-secondary opacity-50">
        Breeze-RP &copy; 2026 | Minimalist Branching Narrative Interface
      </footer>
    </main>
  );
}
