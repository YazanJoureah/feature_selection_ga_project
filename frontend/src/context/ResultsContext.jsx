import React, { createContext, useContext, useState } from "react";

const ResultsContext = createContext();

export const useResults = () => {
  const context = useContext(ResultsContext);
  if (!context) {
    throw new Error("useResults must be used within a ResultsProvider");
  }
  return context;
};

export const ResultsProvider = ({ children }) => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formParams, setFormParams] = useState(null);

  const updateResults = (newResults, params = null) => {
    setResults(newResults);
    if (params) {
      setFormParams(params);
    }
    setError(null);
  };

  const setLoadingState = (isLoading) => {
    setLoading(isLoading);
    if (!isLoading) {
      setError(null);
    }
  };

  const setErrorState = (errorMessage) => {
    setError(errorMessage);
    setLoading(false);
  };

  const clearResults = () => {
    setResults(null);
    setError(null);
    setLoading(false);
    setFormParams(null);
  };

  const updateFormParams = (params) => {
    setFormParams(params);
  };

  return (
    <ResultsContext.Provider
      value={{
        results,
        loading,
        error,
        formParams,
        updateResults,
        setLoadingState,
        setErrorState,
        clearResults,
        updateFormParams,
      }}
    >
      {children}
    </ResultsContext.Provider>
  );
};
