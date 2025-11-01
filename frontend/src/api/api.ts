import axios from 'axios';

const BASE_URL = 'https://feature-selection-ga-project.onrender.com/api';

export const runFeatureSelection = async (formData: FormData) => {
  console.log("Running feature selection with form data ...");
  try {
    const res = await axios.post(`${BASE_URL}/feature-selection`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    console.log("Feature selection completed successfully");
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
