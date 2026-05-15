import api from "@/lib/api";
import { StoryRead, StoryReadSchema, StoryTreeRead, StoryTreeReadSchema } from "../schemas/story-schema";

export const storyApi = {
  create: async (scenarioId: string): Promise<StoryRead> => {
    const response = await api.post(`/stories/?scenario_id=${scenarioId}`);
    return StoryReadSchema.parse(response.data);
  },

  getTree: async (storyId: string): Promise<StoryTreeRead> => {
    const response = await api.get(`/stories/${storyId}/tree`);
    return StoryTreeReadSchema.parse(response.data);
  }
};
