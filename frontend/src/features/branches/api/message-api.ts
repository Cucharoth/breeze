import api from "@/lib/api";

export const messageApi = {
  delete: async (messageId: string): Promise<void> => {
    await api.delete(`/messages/${messageId}`);
  }
};
