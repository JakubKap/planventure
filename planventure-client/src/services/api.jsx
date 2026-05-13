const BASE_URL = 'http://localhost:5000';
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  failedQueue = [];
};

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : '',
  };
};

const handleResponse = async (response) => {
  if (response.status === 401) {
    // Try to refresh token if not already refreshing
    if (!isRefreshing) {
      isRefreshing = true;
      
      try {
        const refreshResponse = await fetch(`${BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        });

        if (refreshResponse.ok) {
          const refreshData = await refreshResponse.json();
          const newToken = refreshData.token || refreshData.access_token;
          
          localStorage.setItem('token', newToken);
          processQueue(null, newToken);
          isRefreshing = false;
          
          // Retry original request with new token
          return fetch(response.url, {
            ...response,
            headers: { ...getAuthHeaders() }
          }).then(handleResponse);
        } else {
          // Refresh failed, logout
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
          processQueue(new Error('Token refresh failed'), null);
          isRefreshing = false;
          throw new Error('Session expired. Please login again.');
        }
      } catch (err) {
        processQueue(err, null);
        isRefreshing = false;
        throw err;
      }
    }

    // While refreshing, queue this request
    return new Promise((resolve, reject) => {
      failedQueue.push({ resolve, reject });
    });
  }

  if (response.status === 404) {
    throw new Error('Trip not found');
  }

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || data.message || 'Request failed');
  }

  console.log('API Response:', data); // Debug log
  return data;
};

export const api = {
  get: async (endpoint) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },
  
  post: async (endpoint, data) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  put: async (endpoint, data) => {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  auth: {
    login: async (credentials) => {
      return api.post('/auth/login', credentials);
    },

    register: async (userData) => {
      return api.post('/auth/register', userData);
    }
  }
};

export default api;