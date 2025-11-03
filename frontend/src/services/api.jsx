import axios from "axios";

const API_BASE_URL = "https://feature-selection-ga-project.onrender.com/api";

// Create axios instance with optimized settings
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 180000, // 3 minutes for complex operations
  headers: {
    "Content-Type": "multipart/form-data",
  },
  // Optimize for large file uploads
  maxContentLength: 50 * 1024 * 1024, // 50MB
  maxBodyLength: 50 * 1024 * 1024, // 50MB
});

// Request optimization for better performance
const optimizeFormData = (formData) => {
  // Remove empty fields and optimize parameters
  const entries = Array.from(formData.entries());
  const optimizedFormData = new FormData();

  entries.forEach(([key, value]) => {
    if (value !== "" && value !== null && value !== undefined) {
      optimizedFormData.append(key, value);
    }
  });

  return optimizedFormData;
};

// Track ongoing requests to avoid duplicates
const pendingRequests = new Map();

// Generate request key for deduplication
const generateRequestKey = (config) => {
  return `${config.method}-${config.url}-${JSON.stringify(config.data)}`;
};

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Optimize form data
    if (config.data instanceof FormData) {
      config.data = optimizeFormData(config.data);
    }

    const requestKey = generateRequestKey(config);

    // Cancel duplicate requests
    if (pendingRequests.has(requestKey)) {
      const cancelSource = pendingRequests.get(requestKey);
      cancelSource.cancel("Duplicate request cancelled");
    }

    // Add cancel token for this request
    const cancelSource = axios.CancelToken.source();
    config.cancelToken = cancelSource.token;
    pendingRequests.set(requestKey, cancelSource);

    console.log(
      "Making API request:",
      config.method?.toUpperCase(),
      config.url
    );
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Remove from pending requests
    const requestKey = generateRequestKey(response.config);
    pendingRequests.delete(requestKey);
    return response;
  },
  (error) => {
    // Remove from pending requests
    if (error.config) {
      const requestKey = generateRequestKey(error.config);
      pendingRequests.delete(requestKey);
    }

    console.error("API Error:", error);

    if (axios.isCancel(error)) {
      throw new Error("Request cancelled");
    }

    if (error.code === "ECONNABORTED") {
      throw new Error(
        "The request is taking longer than expected. This might be due to server load or complex dataset processing. Please try again with simpler parameters."
      );
    }

    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;

      switch (status) {
        case 400:
          throw new Error(
            data.message ||
              "Invalid request. Please check your parameters and try again."
          );
        case 413:
          throw new Error(
            "File too large. Please upload a dataset smaller than 5MB."
          );
        case 429:
          throw new Error(
            "Too many requests. Please wait a few minutes and try again."
          );
        case 500:
          throw new Error(
            data.message ||
              "Server error occurred. Our team has been notified. Please try again later."
          );
        case 502:
        case 503:
          throw new Error(
            "Service temporarily unavailable. The server might be restarting. Please try again in a moment."
          );
        case 504:
          throw new Error(
            "Gateway timeout. The request took too long to process. Please try with a smaller dataset or fewer generations."
          );
        default:
          throw new Error(
            data?.message || `Server error (${status}). Please try again.`
          );
      }
    } else if (error.request) {
      throw new Error(
        "Network connection error. Please check your internet connection and try again."
      );
    } else {
      throw new Error(
        "An unexpected error occurred. Please refresh the page and try again."
      );
    }
  }
);

// Enhanced retry mechanism with exponential backoff
const retryRequest = async (fn, retries = 3, delay = 1000) => {
  try {
    return await fn();
  } catch (error) {
    if (
      retries > 0 &&
      !error.message.includes("cancelled") &&
      !error.message.includes("timeout")
    ) {
      console.log(`Retrying request... ${retries} attempts left`);
      await new Promise((resolve) => setTimeout(resolve, delay));
      return retryRequest(fn, retries - 1, delay * 2);
    }
    throw error;
  }
};

export const featureSelectionAPI = {
  // Single method feature selection
  async singleMethod(formData) {
    return await retryRequest(async () => {
      const response = await api.post("/feature-selection", formData);
      return response.data;
    });
  },

  // Comparison feature selection
  async compareMethods(formData) {
    return await retryRequest(async () => {
      const response = await api.post("/feature-selection/compare", formData);
      return response.data;
    });
  },
};

// Cancel all pending requests
export const cancelAllRequests = () => {
  pendingRequests.forEach((cancelSource, key) => {
    cancelSource.cancel("All requests cancelled");
    pendingRequests.delete(key);
  });
};

export default api;
