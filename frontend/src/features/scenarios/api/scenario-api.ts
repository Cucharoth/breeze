import api from "@/lib/api";
import { Scenario, ScenarioCreate } from "../schemas/scenario-schema";

export const scenarioApi = {
  create: async (data: ScenarioCreate): Promise<Scenario> => {
    const response = await api.post("/scenarios/", data);
    return response.data;
  },

  get: async (id: string): Promise<Scenario> => {
    const response = await api.get(`/scenarios/${id}`);
    return response.data;
  },

  update: async (id: string, data: Partial<Scenario>): Promise<Scenario> => {
    const response = await api.patch(`/scenarios/${id}`, data);
    return response.data;
  }
};
