import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useResults } from "../context/ResultsContext";
import { featureSelectionAPI, cancelAllRequests } from "../services/api";
import LoadingSpinner from "./LoadingSpinner";
import "./HomePage.css";

const HomePage = () => {
  const navigate = useNavigate();
  const {
    setLoadingState,
    setErrorState,
    updateResults,
    updateFormParams,
    loading,
    error,
    clearResults,
  } = useResults();

  const [formData, setFormData] = useState({
    file: null,
    targetColumn: "",
    method: "ga",
    traditional_method: "rfe",
    population_size: 50,
    generations: 50,
    crossover_prob: 0.8,
    mutation_prob: 0.1,
    n_features: 10,
    variance_threshold: 0.01,
  });

  const [localError, setLocalError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fileInputRef = useRef(null);
  const [columns, setColumns] = useState([]);
  const [fileName, setFileName] = useState("");

  // Clear errors when component mounts
  useEffect(() => {
    clearResults();
  }, []);

  // Cancel requests on unmount
  useEffect(() => {
    return () => {
      cancelAllRequests();
    };
  }, []);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        setLocalError(
          "File size too large. Please upload a file smaller than 5MB."
        );
        return;
      }

      // Validate file type
      if (!file.name.toLowerCase().endsWith(".csv")) {
        setLocalError("Please upload a CSV file.");
        return;
      }

      setLocalError("");
      setFormData((prev) => ({ ...prev, file }));
      setFileName(file.name);

      // Read file to get columns
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const content = event.target.result;
          const lines = content.split("\n");
          if (lines.length > 0) {
            const headers = lines[0].split(",").map((h) => h.trim());
            if (headers.length < 2) {
              setLocalError(
                "CSV file must contain at least 2 columns (features and target)"
              );
              return;
            }
            setColumns(headers);
            if (headers.length > 0) {
              setFormData((prev) => ({ ...prev, targetColumn: headers[0] }));
            }
          }
        } catch (error) {
          setLocalError(
            "Error reading CSV file. Please check the file format."
          );
        }
      };
      reader.onerror = () => {
        setLocalError("Error reading file. Please try again.");
      };
      reader.readAsText(file);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "number" ? parseFloat(value) : value,
    }));
    setLocalError("");
    setErrorState(null); // Clear global error when user makes changes
  };

  const validateForm = () => {
    if (!formData.file) {
      return "Please select a CSV file";
    }

    if (!formData.targetColumn) {
      return "Please select a target column";
    }

    if (formData.population_size < 10 || formData.population_size > 200) {
      return "Population size must be between 10 and 200";
    }

    if (formData.generations < 10 || formData.generations > 200) {
      return "Generations must be between 10 and 200";
    }

    if (formData.crossover_prob < 0 || formData.crossover_prob > 1) {
      return "Crossover probability must be between 0 and 1";
    }

    if (formData.mutation_prob < 0 || formData.mutation_prob > 1) {
      return "Mutation probability must be between 0 and 1";
    }

    if (formData.n_features < 1 || formData.n_features > 50) {
      return "Number of features must be between 1 and 50";
    }

    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isSubmitting) return;

    const validationError = validateForm();
    if (validationError) {
      setLocalError(validationError);
      return;
    }

    setIsSubmitting(true);
    setLoadingState(true);
    setErrorState(null);
    setLocalError("");

    // Store form parameters in context
    updateFormParams({
      method: formData.method,
      traditional_method: formData.traditional_method,
      population_size: formData.population_size,
      generations: formData.generations,
      crossover_prob: formData.crossover_prob,
      mutation_prob: formData.mutation_prob,
      n_features: formData.n_features,
      variance_threshold: formData.variance_threshold,
    });

    try {
      const submitData = new FormData();
      submitData.append("file", formData.file);
      submitData.append("target_column", "diagnosis");

      let response;

      if (formData.method === "compare") {
        submitData.append("methods", "ga");
        submitData.append("methods", "traditional");
        submitData.append("population_size", formData.population_size);
        submitData.append("generations", formData.generations);
        submitData.append("traditional_method", formData.traditional_method);
        submitData.append("n_features", formData.n_features);

        response = await featureSelectionAPI.compareMethods(submitData);
      } else {
        submitData.append("method", formData.method);

        if (formData.method === "ga") {
          submitData.append("population_size", formData.population_size);
          submitData.append("generations", formData.generations);
          submitData.append("crossover_prob", formData.crossover_prob);
          submitData.append("mutation_prob", formData.mutation_prob);
        } else {
          submitData.append("traditional_method", formData.traditional_method);
          submitData.append("n_features", formData.n_features);
          if (formData.traditional_method === "variance") {
            submitData.append(
              "variance_threshold",
              formData.variance_threshold
            );
          }
        }

        response = await featureSelectionAPI.singleMethod(submitData);
      }

      updateResults(response, {
        method: formData.method,
        traditional_method: formData.traditional_method,
        population_size: formData.population_size,
        generations: formData.generations,
        crossover_prob: formData.crossover_prob,
        mutation_prob: formData.mutation_prob,
        n_features: formData.n_features,
        variance_threshold: formData.variance_threshold,
      });
      navigate("/results");
    } catch (error) {
      console.error("Submission error:", error);
      setErrorState(error.message);
    } finally {
      setIsSubmitting(false);
      setLoadingState(false);
    }
  };

  const isGA = formData.method === "ga";
  const isTraditional = formData.method === "traditional";
  const isCompare = formData.method === "compare";

  // Show loading spinner when submitting
  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="home-page">
      <div className="upload-section">
        <h2>Upload Your Dataset</h2>

        {/* Global Error Display */}
        {error && (
          <div className="error-banner global-error">
            <div className="error-header">
              <span className="error-icon">⚠️</span>
              <strong>Request Failed</strong>
            </div>
            <p>{error}</p>
            <button className="retry-btn" onClick={() => setErrorState(null)}>
              Dismiss
            </button>
          </div>
        )}

        {/* Local Error Display */}
        {localError && (
          <div className="error-banner local-error">
            <span className="error-icon">❌</span>
            {localError}
          </div>
        )}

        <div
          className={`file-upload-area ${localError ? "error" : ""} ${
            isSubmitting ? "disabled" : ""
          }`}
          onClick={() => !isSubmitting && fileInputRef.current?.click()}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".csv"
            style={{ display: "none" }}
            disabled={isSubmitting}
          />
          <div className="upload-placeholder">
            {fileName ? (
              <>
                <p>✅ {fileName}</p>
                <small>Click to change file</small>
              </>
            ) : (
              <>
                <p>📁 Click to upload CSV file</p>
                <small>Maximum file size: 5MB</small>
              </>
            )}
          </div>
        </div>

        {columns.length > 0 && (
          <form
            onSubmit={handleSubmit}
            className={`config-form ${isSubmitting ? "form-disabled" : ""}`}
          >
            <fieldset disabled={isSubmitting}>
              <div className="form-group">
                <label>Target Column:</label>
                <select
                  name="targetColumn"
                  value={formData.targetColumn}
                  onChange={handleInputChange}
                  required
                >
                  <option value="diagnosis">diagnosis</option>
                </select>
              </div>

              <div className="form-group">
                <label>Method:</label>
                <select
                  name="method"
                  value={formData.method}
                  onChange={handleInputChange}
                >
                  <option value="ga">Genetic Algorithm</option>
                  <option value="traditional">Traditional Method</option>
                  <option value="compare">Compare Methods</option>
                </select>
              </div>

              {/* GA Parameters */}
              {(isGA || isCompare) && (
                <div className="method-params">
                  <h3>Genetic Algorithm Parameters</h3>
                  <div className="param-grid">
                    <div className="param-group">
                      <label>Population Size (10-200):</label>
                      <input
                        type="number"
                        name="population_size"
                        value={formData.population_size}
                        onChange={handleInputChange}
                        min="10"
                        max="200"
                      />
                    </div>
                    <div className="param-group">
                      <label>Generations (10-200):</label>
                      <input
                        type="number"
                        name="generations"
                        value={formData.generations}
                        onChange={handleInputChange}
                        min="10"
                        max="200"
                      />
                    </div>
                    <div className="param-group">
                      <label>Crossover Probability (0-1):</label>
                      <input
                        type="number"
                        name="crossover_prob"
                        value={formData.crossover_prob}
                        onChange={handleInputChange}
                        min="0"
                        max="1"
                        step="0.1"
                      />
                    </div>
                    <div className="param-group">
                      <label>Mutation Probability (0-1):</label>
                      <input
                        type="number"
                        name="mutation_prob"
                        value={formData.mutation_prob}
                        onChange={handleInputChange}
                        min="0"
                        max="1"
                        step="0.01"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Traditional Parameters */}
              {(isTraditional || isCompare) && (
                <div className="method-params">
                  <h3>Traditional Method Parameters</h3>
                  <div className="param-grid">
                    <div className="param-group">
                      <label>Traditional Method:</label>
                      <select
                        name="traditional_method"
                        value={formData.traditional_method}
                        onChange={handleInputChange}
                      >
                        <option value="rfe">RFE</option>
                        <option value="correlation">Correlation</option>
                        <option value="variance">Variance Threshold</option>
                        <option value="kbest">SelectKBest</option>
                      </select>
                    </div>
                    <div className="param-group">
                      <label>Number of Features (1-50):</label>
                      <input
                        type="number"
                        name="n_features"
                        value={formData.n_features}
                        onChange={handleInputChange}
                        min="1"
                        max="50"
                      />
                    </div>
                    {formData.traditional_method === "variance" && (
                      <div className="param-group">
                        <label>Variance Threshold (0-1):</label>
                        <input
                          type="number"
                          name="variance_threshold"
                          value={formData.variance_threshold}
                          onChange={handleInputChange}
                          min="0"
                          max="1"
                          step="0.01"
                        />
                      </div>
                    )}
                  </div>
                </div>
              )}
            </fieldset>

            <div className="form-actions">
              <button
                type="submit"
                className={`submit-btn ${isSubmitting ? "submitting" : ""}`}
                disabled={!formData.file || isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <div className="button-spinner"></div>
                    Processing...
                  </>
                ) : (
                  "Run Feature Selection"
                )}
              </button>
              <p className="estimation-note">
                ⏱️ Estimated processing time: 3-4 minutes
              </p>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default HomePage;
