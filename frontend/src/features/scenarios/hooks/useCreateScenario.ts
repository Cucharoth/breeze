'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { scenarioApi } from '../api/scenario-api';
import { ScenarioCreate, Scenario } from '../schemas/scenario-schema';
import { toast } from 'sonner';

export function useCreateScenario() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const createScenario = async (data: ScenarioCreate) => {
    setIsLoading(true);
    setError(null);

    try {
      const scenario = await scenarioApi.create(data);
      
      toast.success('World generated successfully!');
      console.log('Scenario Created:', scenario);
      
      return scenario;
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Failed to ignite reality. Please try again.';
      setError(message);
      toast.error(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    createScenario,
    isLoading,
    error
  };
}
