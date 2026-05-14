'use client';

import { Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Sparkles, Trees, Feather, Flame, Moon, Mountain, Scroll, Wind, Tent, PenLine, Castle, BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

// Prototype: Storytelling Themes.
// Focus: Dark Scribe / Obsidian Manuscript vibes.

function PrototypeContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const variant = searchParams.get('v') || 'classic';

  const setVariant = (v: string) => {
    router.push(`/prototype?v=${v}`);
  };

  return (
    <div className={cn("min-h-screen relative transition-colors duration-1000 overflow-hidden", 
      variant === 'classic' ? "bg-[#0d110f]" : 
      variant === 'emerald' ? "bg-[#06120b]" : 
      variant === 'stone' ? "bg-[#141414]" : 
      variant === 'noir' ? "bg-[#050505]" : 
      variant === 'campfire' ? "bg-black" : 
      variant === 'scribe' ? "bg-[#1a140f]" : 
      variant === 'obsidian' ? "bg-[#080808]" : "bg-black"
    )}>
      {/* PROTOTYPE HEADER */}
      <div className="fixed top-0 left-0 w-full py-1 text-center font-mono z-[100] uppercase tracking-widest border-b border-white/5 text-[10px] text-white/20">
        Prototype Mode — Storytelling Themes — State: {variant.toUpperCase()}
      </div>

      {/* Variant Switcher */}
      <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-[100] flex items-center gap-2 bg-black/80 backdrop-blur-3xl border border-white/10 p-2 rounded-2xl shadow-2xl max-w-[95vw] overflow-x-auto no-scrollbar">
        <SwitcherBtn active={variant === 'classic'} icon={Trees} label="Tavern" onClick={() => setVariant('classic')} />
        <SwitcherBtn active={variant === 'emerald'} icon={Sparkles} label="Emerald" onClick={() => setVariant('emerald')} />
        <SwitcherBtn active={variant === 'stone'} icon={Mountain} label="Stone" onClick={() => setVariant('stone')} />
        <SwitcherBtn active={variant === 'noir'} icon={Flame} label="Candle" onClick={() => setVariant('noir')} />
        <SwitcherBtn active={variant === 'campfire'} icon={Wind} label="Campfire" onClick={() => setVariant('campfire')} />
        <SwitcherBtn active={variant === 'scribe'} icon={PenLine} label="Scribe" onClick={() => setVariant('scribe')} />
        <SwitcherBtn active={variant === 'obsidian'} icon={BookOpen} label="Obsidian" onClick={() => setVariant('obsidian')} />
      </div>

      {/* Render Variants */}
      <div className="pt-10">
        {variant === 'classic' && <ClassicTavern />}
        {variant === 'emerald' && <EmeraldMist />}
        {variant === 'stone' && <AncientStone />}
        {variant === 'noir' && <CandlelightNoir />}
        {variant === 'campfire' && <CampfireVariant />}
        {variant === 'scribe' && <ScribeVariant />}
        {variant === 'obsidian' && <ObsidianScribeVariant />}
      </div>
    </div>
  );
}

function SwitcherBtn({ active, icon: Icon, label, onClick }: any) {
  return (
    <button 
      onClick={onClick}
      className={cn("flex items-center gap-2 px-6 py-3 rounded-xl transition-all text-sm font-medium whitespace-nowrap", 
        active ? "bg-amber-600 text-white" : "hover:bg-white/5 text-zinc-500")}
    >
      <Icon size={16} /> {label}
    </button>
  );
}

export default function PrototypePage() {
  return (
    <Suspense fallback={<div className="bg-black min-h-screen" />}>
      <PrototypeContent />
    </Suspense>
  );
}

/* --- THE ITERATIONS --- */

function ClassicTavern() {
  return (
    <div className="max-w-4xl mx-auto py-24 px-8 animate-fade-in text-[#d1d5db] font-serif">
      <header className="mb-20 text-center">
        <h1 className="text-6xl font-bold tracking-tighter text-[#2e3d33]">Wilder <span className="text-[#8b4513]">&</span> Tavern</h1>
        <p className="text-[#4a5d50] italic text-lg mt-2">Deep woods, ancient secrets, and a flickering hearth.</p>
      </header>
      <div className="bg-[#1a231e]/60 backdrop-blur-md border-2 border-[#2e3d33] rounded-sm p-12 relative shadow-[20px_20px_0px_#070a09]">
        <textarea className="w-full bg-black/40 border border-[#2e3d33] p-8 text-xl italic outline-none text-[#d1d5db]" rows={5} placeholder="..." />
        <button className="w-full mt-10 bg-[#8b4513] text-white font-bold py-5 text-xl transition-all">Step Into the Dark</button>
      </div>
    </div>
  );
}

function EmeraldMist() {
  return (
    <div className="max-w-4xl mx-auto py-24 px-8 animate-fade-in font-sans text-emerald-50">
      <header className="mb-20 text-center">
        <Sparkles className="text-emerald-400 mx-auto mb-6 animate-pulse" size={40} />
        <h1 className="text-7xl font-light tracking-[0.2em] uppercase text-emerald-400">The Sylvan</h1>
      </header>
      <div className="bg-emerald-950/20 backdrop-blur-3xl border border-emerald-500/20 rounded-[40px] p-16">
        <textarea className="w-full bg-transparent border-b-2 border-emerald-500/10 p-0 text-3xl font-light italic outline-none text-emerald-100" rows={3} placeholder="..." />
        <button className="mt-12 bg-emerald-600 px-12 py-4 rounded-full font-bold text-white">Generate Fate</button>
      </div>
    </div>
  );
}

function AncientStone() {
  return (
    <div className="max-w-4xl mx-auto py-24 px-8 animate-fade-in text-zinc-400 font-serif text-center">
      <header className="mb-20">
        <Mountain className="text-zinc-600 mx-auto mb-6" size={48} />
        <h1 className="text-6xl font-black uppercase text-zinc-100 tracking-tighter">Bastion</h1>
      </header>
      <div className="border-4 border-zinc-800 bg-zinc-900/50 p-12 shadow-[40px_40px_0px_rgba(0,0,0,0.4)]">
        <textarea className="w-full bg-black/40 border-4 border-zinc-800 p-8 text-2xl font-bold outline-none text-zinc-100" rows={4} placeholder="..." />
        <button className="w-full mt-12 bg-zinc-100 text-black font-black py-6 text-2xl uppercase">Engrave</button>
      </div>
    </div>
  );
}

function CandlelightNoir() {
  return (
    <div className="max-w-2xl mx-auto py-32 px-8 animate-fade-in">
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-orange-500/10 blur-[100px] rounded-full pointer-events-none animate-pulse" />
      <header className="mb-24 text-center">
        <Flame className="text-orange-500 mx-auto mb-4 animate-bounce" size={24} />
        <h1 className="text-xs font-mono tracking-[1.5em] uppercase text-orange-500/40">The Inquisitor</h1>
      </header>
      <textarea className="w-full bg-transparent border-none p-0 text-4xl font-serif italic text-zinc-100 outline-none leading-snug" rows={4} placeholder="..." />
      <button className="mt-20 text-orange-500 font-mono text-sm uppercase tracking-[0.4em]">Seal Timeline _</button>
    </div>
  );
}

function CampfireVariant() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center p-8 font-serif animate-fade-in">
      <div className="fixed bottom-[-100px] left-1/2 -translate-x-1/2 w-full h-[400px] bg-orange-600/30 blur-[120px] rounded-full pointer-events-none animate-pulse" />
      <div className="max-w-3xl w-full relative z-10">
        <Flame className="text-orange-600 mx-auto mb-6" size={48} />
        <h1 className="text-5xl font-black text-orange-100 text-center italic mb-12">Campfire Tales</h1>
        <div className="bg-zinc-900/40 backdrop-blur-sm border-2 border-orange-900/20 p-12 rounded-[60px] shadow-2xl">
          <textarea className="w-full bg-transparent border-none text-2xl italic outline-none text-orange-50 placeholder:text-orange-900/30" placeholder="..." />
          <button className="w-full mt-10 bg-orange-600 text-black font-black py-5 rounded-full text-lg uppercase tracking-widest">Stoke the Fire</button>
        </div>
      </div>
    </div>
  );
}

function ScribeVariant() {
  return (
    <div className="max-w-4xl mx-auto py-24 px-8 animate-fade-in font-serif text-[#3d2b1f]">
      <div className="absolute inset-0 opacity-[0.15] pointer-events-none" style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/dark-wood.png")' }} />
      <div className="fixed top-[15%] right-[20%] w-[400px] h-[400px] bg-amber-500/10 blur-[100px] rounded-full pointer-events-none" />
      <header className="mb-20 text-center relative z-10">
        <Castle className="text-[#8b4513]/40 mx-auto mb-6" size={56} />
        <h1 className="text-6xl font-bold tracking-tight text-[#d1d5db]">The Scribe's Manor</h1>
        <p className="text-[#8b4513] italic text-xl mt-2 font-light">Ink, parchment, and the weight of legacy.</p>
      </header>
      <div className="relative max-w-2xl mx-auto group">
        <div className="absolute -inset-2 bg-[#b8a270] rotate-1 shadow-sm rounded-sm" />
        <div className="absolute -inset-1 bg-[#c4b38d] -rotate-1 shadow-md rounded-sm" />
        <div className="relative bg-[#d1bc8a] p-16 shadow-2xl rounded-sm border-t-[32px] border-[#b8a270] min-h-[500px]">
          <textarea 
            className="w-full bg-transparent border-none text-2xl outline-none placeholder:text-[#3d2b1f]/20 leading-[2.2rem] resize-none overflow-hidden text-[#1a120b] font-medium" 
            rows={8}
            placeholder="Upon this day, I record the following events..."
            style={{ backgroundImage: 'linear-gradient(transparent, transparent 34px, rgba(0,0,0,0.05) 34px, rgba(0,0,0,0.05) 35px)', backgroundSize: '100% 35px' }}
          />
          <div className="mt-16 flex flex-col items-center gap-6">
            <button className="group relative flex flex-col items-center gap-2 transition-all">
              <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-[#8b4513]/50 group-hover:text-[#8b4513] transition-colors">Apply Seal</span>
              <div className="w-16 h-16 rounded-full bg-red-900 shadow-lg border-4 border-red-950 flex items-center justify-center text-white/40 font-black text-2xl group-hover:scale-110 active:scale-95 transition-all">B</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function ObsidianScribeVariant() {
  return (
    <div className="max-w-4xl mx-auto py-24 px-8 animate-fade-in font-serif text-amber-500/80">
      {/* Deep Dark Wood Background */}
      <div className="absolute inset-0 opacity-[0.2] pointer-events-none" style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/black-linen.png")' }} />
      
      {/* Cold Moonlight / Amber Glow */}
      <div className="fixed top-[10%] left-[10%] w-[500px] h-[500px] bg-amber-900/10 blur-[150px] rounded-full pointer-events-none" />
      <div className="fixed bottom-[10%] right-[10%] w-[400px] h-[400px] bg-zinc-900/20 blur-[120px] rounded-full pointer-events-none" />

      <header className="mb-20 text-center relative z-10">
        <BookOpen className="text-amber-700/40 mx-auto mb-6" size={56} />
        <h1 className="text-6xl font-black tracking-widest text-zinc-100 uppercase italic">Obsidian <span className="text-amber-600">Manuscript</span></h1>
        <p className="text-amber-700 italic text-lg mt-4 font-light tracking-widest">Inscribed in shadow, illuminated by truth.</p>
      </header>

      <div className="relative max-w-2xl mx-auto group">
        {/* Dark Parchment Layers */}
        <div className="absolute -inset-3 bg-zinc-900/50 rotate-[-1deg] shadow-2xl rounded-sm border border-white/5" />
        <div className="absolute -inset-1 bg-zinc-900 rotate-[0.5deg] shadow-2xl rounded-sm border border-white/5" />
        
        {/* Main Dark Paper */}
        <div className="relative bg-[#161616] p-16 shadow-[0_0_100px_rgba(0,0,0,0.5)] rounded-sm border-t-[40px] border-[#1a1a1a] min-h-[550px] overflow-hidden">
          {/* Subtle Texture Overlay */}
          <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'url("https://www.transparenttextures.com/patterns/noise-lines.png")' }} />
          
          <div className="flex items-center gap-6 mb-12 opacity-20">
            <Feather size={24} className="text-amber-500" />
            <div className="h-[1px] flex-1 bg-gradient-to-r from-amber-900 via-amber-900/10 to-transparent" />
          </div>

          <textarea 
            className="w-full bg-transparent border-none text-2xl outline-none placeholder:text-zinc-800 leading-[2.5rem] resize-none overflow-hidden text-amber-500/90 font-light italic" 
            rows={8}
            placeholder="The void begins to speak..."
            style={{ 
              backgroundImage: 'linear-gradient(transparent, transparent 39px, rgba(251, 191, 36, 0.05) 39px, rgba(251, 191, 36, 0.05) 40px)', 
              backgroundSize: '100% 40px',
              textShadow: '0 0 10px rgba(251, 191, 36, 0.2)' 
            }}
          />

          <div className="mt-16 flex flex-col items-center gap-8 relative z-10">
            <div className="h-[1px] w-32 bg-gradient-to-r from-transparent via-amber-900/30 to-transparent" />
            <button className="group relative transition-all">
              <div className="absolute -inset-4 bg-amber-600/5 blur-xl group-hover:bg-amber-600/20 transition-all rounded-full" />
              <div className="relative w-20 h-20 rounded-full bg-zinc-900 border-2 border-amber-900/50 flex items-center justify-center text-amber-600 shadow-2xl group-hover:border-amber-500 group-hover:text-amber-400 transition-all">
                <Flame size={32} className="group-hover:animate-pulse" />
              </div>
              <span className="block mt-4 text-[9px] uppercase tracking-[0.6em] font-bold text-amber-900 group-hover:text-amber-600 text-center transition-colors">Ignite Reality</span>
            </button>
          </div>
        </div>
      </div>

      <div className="mt-24 flex justify-between px-10 opacity-10 text-[9px] font-mono uppercase tracking-[0.5em] text-white">
        <span>Fragment_#812</span>
        <span>Status: Unsealed</span>
        <span>Epoch: Null</span>
      </div>
    </div>
  );
}
