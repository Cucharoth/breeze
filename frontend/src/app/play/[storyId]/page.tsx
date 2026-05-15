import { storyApi } from '@/features/stories/api/story-api';
import { scenarioApi } from '@/features/scenarios/api/scenario-api';
import { branchApi } from '@/features/branches/api/branch-api';
import PlayClient from './PlayClient';
import { notFound } from 'next/navigation';

interface PlayPageProps {
  params: Promise<{ storyId: string }>;
  searchParams: Promise<{ branch?: string }>;
}

export default async function PlayPage({ params, searchParams }: PlayPageProps) {
  const { storyId } = await params;
  const { branch: branchId } = await searchParams;
  
  if (!storyId) notFound();

  // 1. Fetch initial data
  let tree;
  let scenario;
  try {
    tree = await storyApi.getTree(storyId);
    scenario = await scenarioApi.get(tree.scenario_id);
  } catch (err) {
    notFound();
  }

  const activeBranchId = branchId || tree.story_id; 
  
  // 2. Fetch History for the active branch
  let history: { id: string; branch_id: string; role: "user" | "assistant" | "system"; content: string; created_at: string; }[] = [];
  try {
    history = await branchApi.getHistory(activeBranchId);
  } catch (err) {
    console.error("Failed to load history", err);
  }
  
  return (
    <main className="relative min-h-screen w-full overflow-hidden bg-stone-950 text-stone-200">
      {/* Dynamic Theme Background */}
      <div className="absolute inset-0 z-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-amber-900/10 via-stone-950 to-stone-950 opacity-50" />
      
      <PlayClient 
        initialScenario={scenario}
        initialHistory={history}
        storyId={storyId}
        activeBranchId={activeBranchId}
      />
    </main>
  );
}
