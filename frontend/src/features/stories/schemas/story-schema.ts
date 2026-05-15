import { z } from 'zod';

export const StoryBaseSchema = z.object({
  scenario_id: z.string(),
});

export const StoryReadSchema = StoryBaseSchema.extend({
  id: z.string(),
  main_branch_id: z.string().nullable(),
});

export const BranchTreeNodeSchema = z.object({
  id: z.string(),
  name: z.string(),
  parent_checkpoint_id: z.string().nullable(),
});

export const CheckpointTreeNodeSchema = z.object({
  id: z.string(),
  branch_id: z.string(),
  message_id: z.string(),
});

export const StoryTreeReadSchema = z.object({
  story_id: z.string(),
  scenario_id: z.string(),
  branches: z.array(BranchTreeNodeSchema),
  checkpoints: z.array(CheckpointTreeNodeSchema),
});

export type StoryRead = z.infer<typeof StoryReadSchema>;
export type StoryTreeRead = z.infer<typeof StoryTreeReadSchema>;
