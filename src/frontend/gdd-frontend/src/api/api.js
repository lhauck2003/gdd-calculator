// src/api/api.js
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const fetchFields = async () => {
  const res = await axios.get(`${API_BASE}/fields/`);
  return res.data;
};

export const fetchPlantedCrops = async () => {
  const res = await axios.get(`${API_BASE}/plantedcrops/`);
  return res.data;
};