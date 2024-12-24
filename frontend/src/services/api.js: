import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const registerUser = (userData) => {
  return axios.post(`${API_URL}/register/user`, userData);
};

export const registerStore = (storeData) => {
  return axios.post(`${API_URL}/register/store`, storeData);
};

export const loginUser = (userData) => {
  return axios.post(`${API_URL}/login/user`, userData);
};

export const loginStore = (storeData) => {
  return axios.post(`${API_URL}/login/store`, storeData);
};

export const recordTransaction = (transactionData) => {
  return axios.post(`${API_URL}/transaction`, transactionData);
};

export const getUserCredits = (userId) => {
  return axios.get(`${API_URL}/credits/user/${userId}`);
};

export const getStoreCredits = (storeId) => {
  return axios.get(`${API_URL}/credits/store/${storeId}`);
};