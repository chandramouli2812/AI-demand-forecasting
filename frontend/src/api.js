import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api"; // ✅ IMPORTANT

export const uploadFile = async (formData) => {
  return await axios.post(`${BASE_URL}/upload`, formData);
};

export const trainModel = async () => {
  return await axios.post(`${BASE_URL}/train`);
};

export const getPrediction = async (days = 7) => {
  return await axios.get(`${BASE_URL}/predict?days=${days}`);
};

export const getInsights = async () => {
  return await axios.get(`${BASE_URL}/insights`);
};