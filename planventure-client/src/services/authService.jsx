import { api } from './api';

export const authService = {
  login: async (credentials) => {
    return await api.post('/auth/login', credentials);
  },

  register: async (userData) => {
    return await api.post('/auth/register', userData);
  },

  refreshToken: async () => {
    return await api.post('/auth/refresh', {});
  },

  logout: async () => {
    return await api.post('/auth/logout', {});
  }
};