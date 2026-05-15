import { z } from 'zod';

export const BranchBaseSchema = z.object({
  name: z.string().max(100),
  short_term_directive: z.string().max(500).nullable().optional(),
  long_term_directive: z.string().max(1000).nullable().optional(),
});

export const BranchReadSchema = BranchBaseSchema.extend({
  id: z.string(),
  story_id: z.string(),
  parent_checkpoint_id: z.string().nullable(),
});

export const MessageReadSchema = z.object({
  id: z.string(),
  branch_id: z.string(),
  role: z.enum(['user', 'assistant', 'system']),
  content: z.string(),
  created_at: z.string(),
});

export type BranchRead = z.infer<typeof BranchReadSchema>;
export type MessageRead = z.infer<typeof MessageReadSchema>;
