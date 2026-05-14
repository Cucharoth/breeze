import { z } from 'zod';

export const ScenarioCreateSchema = z.object({
  premise: z.string().min(5).max(500),
});

export type ScenarioCreate = z.infer<typeof ScenarioCreateSchema>;

export const ScenarioSchema = ScenarioCreateSchema.extend({
  id: z.number(),
  world_lore: z.string(),
  first_scene: z.string(),
  character_profiles: z.array(z.any()),
});

export type Scenario = z.infer<typeof ScenarioSchema>;
