import axios from 'axios';
import { logger } from './logger';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  timeout: 20000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  logger.debug(`🚀 Request: ${config.method?.toUpperCase()} ${config.url}`);
  return config;
});

api.interceptors.response.use(
  (response) => {
    logger.debug(`✅ Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    logger.error(`❌ API Error: ${error.response?.status} ${error.config?.url}`, error.message);
    return Promise.reject(error);
  }
);

export default api;
