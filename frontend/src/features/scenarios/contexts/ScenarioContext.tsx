'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Scenario } from '../schemas/scenario-schema';
import { scenarioApi } from '../api/scenario-api';
import { toast } from 'sonner';

interface ScenarioContextType {
  scenario: Scenario | null;
  setScenario: (scenario: Scenario) => void;
  updateScenario: (data: Partial<Scenario>) => Promise<void>;
  refreshScenario: (id: string) => Promise<void>;
}

const ScenarioContext = createContext<ScenarioContextType | undefined>(undefined);

export function ScenarioProvider({ 
  initialScenario, 
  children 
}: { 
  initialScenario: Scenario; 
  children: ReactNode 
}) {
  const [scenario, setScenarioState] = useState<Scenario>(initialScenario);

  const updateScenario = async (data: Partial<Scenario>) => {
    try {
      const updated = await scenarioApi.update(scenario.id, data);
      setScenarioState(updated);
    } catch (err) {
      toast.error('Failed to update the manuscript.');
      throw err;
    }
  };

  const refreshScenario = async (id: string) => {
    try {
      const fresh = await scenarioApi.get(id);
      setScenarioState(fresh);
    } catch (err) {
      console.error('Failed to refresh scenario', err);
    }
  };

  return (
    <ScenarioContext.Provider value={{ 
      scenario, 
      setScenario: setScenarioState, 
      updateScenario,
      refreshScenario
    }}>
      {children}
    </ScenarioContext.Provider>
  );
}

export function useScenario() {
  const context = useContext(ScenarioContext);
  if (context === undefined) {
    throw new Error('useScenario must be used within a ScenarioProvider');
  }
  return context;
}
