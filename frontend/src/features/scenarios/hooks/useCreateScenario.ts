'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { scenarioApi } from '../api/scenario-api';
import { ScenarioCreate, Scenario } from '../schemas/scenario-schema';
import { toast } from 'sonner';
import { logger } from '@/lib/logger';
import { storyApi } from '../../stories/api/story-api';

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
      logger.debug('Scenario Created: ', scenario);
      
      // Step 2: Create a Story from the Scenario
      toast.loading('Igniting your story...');
      const story = await storyApi.create(scenario.id);
      
      // Step 3: Navigate to the play page
      router.push(`/play/${story.id}?branch=${story.main_branch_id}`);
      
      return scenario;
    } catch (err: any) {
      const message = err.response?.data?.detail || 'Failed to ignite reality. Please try again.';
      setError(message);
      toast.error(message);
      logger.debug('Scenario Creation Failed: ', err);
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
