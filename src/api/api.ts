import axios from 'axios';

// Use Vite env variable VITE_API_BASE_URL when available, otherwise fallback to the hosted URL.
// Set VITE_API_BASE_URL in a .env or .env.local file at the project root during development.
const FALLBACK_BASE = 'https://feature-selection-ga-project.onrender.com/api';
const BASE_URL = (import.meta.env.VITE_API_BASE_URL as string) || FALLBACK_BASE;

export const runFeatureSelection = async (formData: FormData) => {
  try {
    const res = await axios.post(`${BASE_URL}/feature-selection`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  } catch (err) {
    // normalize axios error for callers
    if (axios.isAxiosError(err)) {
      const message = err.response?.data?.message || err.message;
      throw new Error(`API error: ${message}`);
    }
    throw err;
  }
};
