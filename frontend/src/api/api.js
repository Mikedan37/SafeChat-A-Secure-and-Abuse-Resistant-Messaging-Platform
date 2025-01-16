// api.js
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000/api';

export const registerUser = (data) => axios.post(`${API_BASE}/register`, data);

export const loginUser = async (credentials) => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/login', credentials);
    return response;
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};

export const fetchProfile = (token) => axios.get(`${API_BASE}/profile`, {
  headers: { Authorization: `Bearer ${token}` },
});
export const sendMessage = (data, token) =>
  axios.post(`${API_BASE}/send_message`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });
export const fetchThread = (threadId, token) =>
  axios.get(`${API_BASE}/get_thread/${threadId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
export const enable2FA = (token) =>
  axios.post(`${API_BASE}/enable_2fa`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  });
export const deleteUser = (data, token) =>
  axios.delete(`${API_BASE}/delete_user`, {
    headers: { Authorization: `Bearer ${token}` },
    data,
  });