import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000/api";

export const uploadFile = async (formData) => {
  return await axios.post(`${BASE_URL}/upload`, formData);
};

export const trainModel = async () => {
  return await axios.post(`${BASE_URL}/train`);
};

export const getPrediction = async (days = 7, product = "All Products") => {
  const encodedProduct = encodeURIComponent(product || "All Products");
  return await axios.get(`${BASE_URL}/predict?days=${days}&product=${encodedProduct}`);
};

export const getInsights = async (product = "All Products") => {
  const query = product ? `?product=${encodeURIComponent(product)}` : "";
  return await axios.get(`${BASE_URL}/insights${query}`);
};