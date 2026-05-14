import { ScenarioForm } from "@/features/scenarios/components/ScenarioForm";
import { ThemeSelector } from "@/components/ui/ThemeSelector";
import { ThemeEffects } from "@/components/ThemeEffects";

export default function Home() {
  return (
    <main className="main-container animate-fade-in relative">
      <ThemeEffects />
      
      <div className="fixed top-8 right-8 z-[100]">
        <ThemeSelector />
      </div>

      <header className="mb-20 text-center relative z-10">
        <h1 className="text-[4.5rem] font-extrabold tracking-tight italic">
          Breeze<span className="text-primary">.</span>
        </h1>
        <p className="text-xl opacity-80 italic">
          Crafting parallel timelines with a single breath.
        </p>
      </header>

      <div className="relative z-10">
        <ScenarioForm />
      </div>
      
      <footer className="mt-32 text-center text-[0.8rem] text-text-secondary opacity-50 relative z-10">
        Breeze-RP &copy; 2026 | Minimalist Branching Narrative Interface
      </footer>
    </main>
  );
}
