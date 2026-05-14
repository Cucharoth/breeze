import api from "@/lib/api";
import { Scenario, ScenarioCreate } from "../schemas/scenario-schema";

export const scenarioApi = {
  create: async (data: ScenarioCreate): Promise<Scenario> => {
    const response = await api.post("/scenarios/", data);
    return response.data;
  },
};
