'use client';

import { useState } from 'react';
import { useScenario } from '../contexts/ScenarioContext';
import { toast } from 'sonner';

export default function LoreSidebar() {
  const { scenario, updateScenario } = useScenario();
  
  // World Lore Editing
  const [isEditingLore, setIsEditingLore] = useState(false);
  const [editingLore, setEditingLore] = useState(scenario?.world_lore || '');

  // Characters Editing
  const [editingActorIdx, setEditingActorIdx] = useState<number | null>(null);
  const [editingActorName, setEditingActorName] = useState('');
  const [editingActorDesc, setEditingActorDesc] = useState('');

  // Drag and Drop state
  const [draggedIdx, setDraggedIdx] = useState<number | null>(null);

  if (!scenario) return null;

  const saveLore = async () => {
    try {
      await updateScenario({ world_lore: editingLore });
      setIsEditingLore(false);
      toast.success('The World Lore has been reshaped.');
    } catch (err) {
      toast.error('The manuscript resisted your changes.');
    }
  };

  const startEditActor = (idx: number) => {
    setEditingActorIdx(idx);
    setEditingActorName(scenario.character_profiles[idx].name);
    setEditingActorDesc(scenario.character_profiles[idx].description);
  };

  const saveActor = async () => {
    if (editingActorIdx === null) return;
    
    const newProfiles = [...scenario.character_profiles];
    newProfiles[editingActorIdx] = {
      ...newProfiles[editingActorIdx],
      name: editingActorName,
      description: editingActorDesc
    };
    
    try {
      await updateScenario({ character_profiles: newProfiles });
      setEditingActorIdx(null);
      toast.success(`${editingActorName}'s destiny has been updated.`);
    } catch (err) {
      toast.error('The manifestation could not be altered.');
    }
  };

  const startAddActor = () => {
    setEditingActorIdx(-1);
    setEditingActorName('New Actor');
    setEditingActorDesc('');
  };

  const saveNewActor = async () => {
    const newActor = { name: editingActorName, description: editingActorDesc, role: "NPC" };
    const newProfiles = [...scenario.character_profiles, newActor];
    
    try {
      await updateScenario({ character_profiles: newProfiles });
      setEditingActorIdx(null);
      toast.success('A new entity has emerged.');
    } catch (err) {
      toast.error('Failed to summon the new actor.');
    }
  };

  const deleteActor = async (idx: number) => {
    const actorName = scenario.character_profiles[idx].name;
    const newProfiles = scenario.character_profiles.filter((_, i) => i !== idx);
    
    try {
      await updateScenario({ character_profiles: newProfiles });
      toast.info(`${actorName} has faded from existence.`);
    } catch (err) {
      toast.error('Failed to banish the actor.');
    }
  };

  // Drag and Drop Handlers
  const handleDragStart = (idx: number) => {
    setDraggedIdx(idx);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = async (targetIdx: number) => {
    if (draggedIdx === null || draggedIdx === targetIdx) return;
    
    const newProfiles = [...scenario.character_profiles];
    const [draggedItem] = newProfiles.splice(draggedIdx, 1);
    newProfiles.splice(targetIdx, 0, draggedItem);
    
    setDraggedIdx(null);
    try {
      await updateScenario({ character_profiles: newProfiles });
      toast.success('Temporal order rearranged.');
    } catch (err) {
      toast.error('Failed to reorder destiny.');
    }
  };

  return (
    <div className="flex flex-col h-full bg-stone-900/40 backdrop-blur-xl border-l border-stone-800/50 select-none">
      <div className="p-6 border-b border-stone-800/50 bg-stone-950/20">
         <h1 className="font-serif text-xl text-amber-500/90 tracking-wide">Codex of Reality</h1>
         <p className="text-[10px] text-stone-500 uppercase tracking-[0.2em] mt-1">Lore & Manifestations</p>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-10 scrollbar-hide">
        {/* World Lore Section */}
        <section className="relative">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-[10px] font-bold text-stone-500 uppercase tracking-widest flex items-center gap-2">
              <span className="h-1 w-1 bg-amber-600 rounded-full" />
              Primal Lore
            </h2>
            <button 
              onClick={() => isEditingLore ? saveLore() : setIsEditingLore(true)}
              className="text-[10px] text-amber-600/80 hover:text-amber-400 uppercase font-bold transition-colors"
            >
              {isEditingLore ? 'Seal' : 'Reshape'}
            </button>
          </div>
          
          {isEditingLore ? (
            <div className="space-y-3 animate-in fade-in zoom-in-95 duration-300">
              <textarea 
                value={editingLore}
                onChange={(e) => setEditingLore(e.target.value)}
                className="w-full h-64 bg-stone-950/50 border border-amber-900/30 rounded-lg p-4 text-sm text-stone-200 focus:outline-none focus:border-amber-700/50 transition-all font-serif leading-relaxed"
                placeholder="Rewrite the laws of this world..."
              />
            </div>
          ) : (
            <div className="group relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-amber-900/5 to-transparent rounded-lg blur opacity-25 group-hover:opacity-50 transition duration-1000"></div>
              <div className="relative p-5 rounded-lg border border-stone-800 bg-stone-950/40 leading-relaxed font-serif text-stone-400 text-sm italic">
                {scenario.world_lore}
              </div>
            </div>
          )}
        </section>

        {/* Characters Section */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-[10px] font-bold text-stone-500 uppercase tracking-widest flex items-center gap-2">
              <span className="h-1 w-1 bg-amber-600 rounded-full" />
              Active Actors
            </h2>
            <button 
              onClick={startAddActor}
              className="text-[10px] text-stone-600 hover:text-amber-500 uppercase font-bold transition-colors flex items-center gap-1"
            >
              <span className="text-sm">+</span> Summon
            </button>
          </div>
          
          <div className="grid gap-4">
            {editingActorIdx === -1 && (
               <div className="p-4 rounded-lg border border-amber-500/50 bg-stone-900/50 space-y-3 animate-in slide-in-from-top-2 duration-300 shadow-[0_0_15px_rgba(245,158,11,0.1)]">
                 <input 
                   autoFocus
                   value={editingActorName}
                   onChange={(e) => setEditingActorName(e.target.value)}
                   className="w-full bg-transparent border-b border-stone-800 py-1 text-sm font-serif text-amber-100 focus:outline-none focus:border-amber-700/50"
                   placeholder="Actor Name"
                 />
                 <textarea 
                   value={editingActorDesc}
                   onChange={(e) => setEditingActorDesc(e.target.value)}
                   className="w-full h-24 bg-transparent text-xs text-stone-400 focus:outline-none resize-none leading-relaxed"
                   placeholder="Describe essence..."
                 />
                 <div className="flex justify-end gap-2">
                   <button onClick={() => setEditingActorIdx(null)} className="text-[10px] text-stone-600 uppercase font-bold px-2 py-1">Cancel</button>
                   <button onClick={saveNewActor} className="text-[10px] text-amber-600 uppercase font-bold border border-amber-900/30 px-3 py-1 rounded hover:bg-amber-900/10 transition-all">Summon</button>
                 </div>
               </div>
            )}

            {scenario.character_profiles.map((char: any, idx: number) => (
              <div 
                key={idx} 
                draggable={editingActorIdx === null}
                onDragStart={() => handleDragStart(idx)}
                onDragOver={handleDragOver}
                onDrop={() => handleDrop(idx)}
                className={`relative group ${draggedIdx === idx ? 'opacity-20' : ''} cursor-grab active:cursor-grabbing transition-opacity`}
              >
                {editingActorIdx === idx ? (
                  <div className="p-4 rounded-lg border border-amber-900/30 bg-stone-950/60 space-y-3">
                    <input 
                      value={editingActorName}
                      onChange={(e) => setEditingActorName(e.target.value)}
                      className="w-full bg-transparent border-b border-stone-800 py-1 text-sm font-serif text-amber-100 focus:outline-none"
                    />
                    <textarea 
                      value={editingActorDesc}
                      onChange={(e) => setEditingActorDesc(e.target.value)}
                      className="w-full h-24 bg-transparent text-xs text-stone-400 focus:outline-none resize-none"
                    />
                    <div className="flex justify-end gap-2">
                      <button onClick={() => setEditingActorIdx(null)} className="text-[10px] text-stone-600 uppercase font-bold px-2 py-1">Cancel</button>
                      <button onClick={saveActor} className="text-[10px] text-amber-600 uppercase font-bold border border-amber-900/30 px-3 py-1 rounded">Save</button>
                    </div>
                  </div>
                ) : (
                  <div className="p-4 rounded-lg border border-stone-800 bg-stone-950/30 group-hover:border-amber-900/20 transition-all duration-300">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                         <div className="h-1.5 w-1.5 rounded-full bg-stone-800 group-hover:bg-amber-600 transition-colors" />
                         <p className="text-sm font-serif text-stone-200 group-hover:text-amber-200/80 transition-colors">{char.name}</p>
                      </div>
                      <div className="flex items-center gap-3 opacity-0 group-hover:opacity-100 transition-all">
                        <button onClick={() => startEditActor(idx)} className="text-[9px] text-stone-500 hover:text-amber-600 uppercase font-bold">Edit</button>
                        <button onClick={() => deleteActor(idx)} className="text-[9px] text-stone-600 hover:text-red-900 uppercase font-bold">×</button>
                      </div>
                    </div>
                    <p className="text-xs text-stone-500 leading-relaxed line-clamp-2">
                      {char.description}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      </div>
      
      <div className="p-6 border-t border-stone-800/50 bg-stone-950/20">
         <div className="flex items-center gap-3 text-[10px] text-stone-600 uppercase tracking-wider">
            <span className="h-1.5 w-1.5 rounded-full bg-amber-900/30 animate-pulse" />
            Reality Synced
         </div>
      </div>
    </div>
  );
}
