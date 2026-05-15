import api from "@/lib/api";
import { MessageReadSchema, MessageRead } from "../schemas/branch-schema";
import { z } from "zod";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const branchApi = {
  getHistory: async (branchId: string): Promise<MessageRead[]> => {
    const response = await api.get(`/branches/${branchId}/history/`);
    return z.array(MessageReadSchema).parse(response.data);
  },

  // Streaming endpoint using native fetch
  streamNext: async (branchId: string, onToken: (token: string) => void): Promise<void> => {
    const response = await fetch(`${BASE_URL}/branches/${branchId}/stream-next`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) throw new Error('Streaming failed');
    if (!response.body) throw new Error('No response body');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const token = decoder.decode(value, { stream: true });
      onToken(token);
    }
  },

  deleteLastMessage: async (branchId: string): Promise<boolean> => {
    const response = await api.delete(`/branches/${branchId}/last-message`);
    return response.data.deleted;
  }
};
