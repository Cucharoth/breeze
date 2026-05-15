'use client';

import { ScenarioProvider } from '@/features/scenarios/contexts/ScenarioContext';
import { Scenario } from '@/features/scenarios/schemas/scenario-schema';
import { MessageRead } from '@/features/branches/schemas/branch-schema';
import Chat from '@/features/branches/components/Chat';
import LoreSidebar from '@/features/scenarios/components/LoreSidebar';
import { useScenario } from '@/features/scenarios/contexts/ScenarioContext';

interface PlayClientProps {
  initialScenario: Scenario;
  initialHistory: MessageRead[];
  storyId: string;
  activeBranchId: string;
}

function PlayContent({ initialHistory, activeBranchId }: { initialHistory: MessageRead[], activeBranchId: string }) {
  const { scenario } = useScenario();
  
  if (!scenario) return null;

  return (
    <div className="relative z-10 flex h-screen w-full">
      {/* Left Sidebar: Chronos Tree */}
      <aside className="w-80 border-r border-stone-800/50 bg-stone-900/30 backdrop-blur-md hidden xl:block">
        <div className="p-6">
          <h2 className="font-serif text-xl font-bold tracking-tight text-amber-500/80">Chronos Tree</h2>
          <p className="mt-1 text-xs text-stone-500 uppercase tracking-widest">Temporal Branches</p>
        </div>
        <div className="px-6 py-4 border-t border-stone-800/30 text-sm text-stone-400 italic">
          Tree visualization coming soon...
        </div>
      </aside>

      {/* Central Workspace: The Manuscript */}
      <section className="flex-1 flex flex-col h-full overflow-hidden">
        <header className="flex h-16 items-center justify-between border-b border-stone-800/50 bg-stone-950/50 px-8 backdrop-blur-sm shrink-0">
          <div className="flex items-center gap-4">
             <span className="h-2 w-2 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)]" />
             <h1 className="font-serif text-lg text-stone-300">The Obsidian Manuscript</h1>
          </div>
          <div className="flex gap-4">
            <button className="text-[10px] uppercase tracking-widest text-stone-500 hover:text-amber-500 transition-colors">Save Timeline</button>
          </div>
        </header>

        <Chat 
          branchId={activeBranchId} 
          initialHistory={initialHistory} 
        />
      </section>

      {/* Right Sidebar: Codex of Reality */}
      <aside className="w-[450px] border-l border-stone-800/50 bg-stone-900/30 backdrop-blur-md hidden lg:block overflow-hidden">
        <LoreSidebar />
      </aside>
    </div>
  );
}

export default function PlayClient({ 
  initialScenario, 
  initialHistory, 
  activeBranchId 
}: PlayClientProps) {
  return (
    <ScenarioProvider initialScenario={initialScenario}>
      <PlayContent initialHistory={initialHistory} activeBranchId={activeBranchId} />
    </ScenarioProvider>
  );
}
