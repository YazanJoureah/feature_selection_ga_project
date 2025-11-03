import React from "react";
import { useNavigate } from "react-router-dom";
import { useResults } from "../context/ResultsContext";
import ResultsOverview from "./ResultsOverview";
import FeatureQualityChart from "./FeatureQualityChart";
import FeatureOverlapChart from "./FeatureOverlapChart";
import PerformanceComparisonChart from "./PerformanceComparisonChart";
import SelectedFeatures from "./SelectedFeatures";
import "./ResultsPage.css";

const ResultsPage = () => {
  const { results, loading, error, formParams } = useResults();
  const navigate = useNavigate();

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Running feature selection analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={() => navigate("/")}>Back to Home</button>
      </div>
    );
  }

  if (!results) {
    navigate("/");
    return null;
  }

  const isComparison = results.method_used === "Comparison (ga, traditional)";
  const hasGA = results.results?.ga;
  const hasTraditional = results.results?.traditional;

  // Get the traditional method name from form parameters
  const getTraditionalMethodName = () => {
    if (!formParams) return "Traditional";

    const method = formParams.traditional_method;
    switch (method) {
      case "rfe":
        return "RFE";
      case "correlation":
        return "Correlation";
      case "variance":
        return "Variance Threshold";
      case "kbest":
        return "SelectKBest";
      default:
        return "Traditional";
    }
  };

  // Get the main method type
  const getMainMethod = () => {
    return formParams?.method || "ga";
  };

  // Dynamic badge generation based on form parameters
  const getMethodBadges = () => {
    const mainMethod = getMainMethod();
    const traditionalMethodName = getTraditionalMethodName();

    if (mainMethod === "compare") {
      return (
        <>
          <span className="badge ga">Genetic Algorithm</span>
          <span
            className={`badge traditional ${traditionalMethodName
              .toLowerCase()
              .replace(" ", "-")}`}
          >
            {traditionalMethodName}
          </span>
        </>
      );
    } else if (mainMethod === "ga") {
      return <span className="badge ga">Genetic Algorithm</span>;
    } else {
      return (
        <span
          className={`badge ${traditionalMethodName
            .toLowerCase()
            .replace(" ", "-")}`}
        >
          {traditionalMethodName}
        </span>
      );
    }
  };

  // Get display title for traditional method features
  const getTraditionalMethodTitle = () => {
    const methodName = getTraditionalMethodName();
    return `${methodName} Selected Features`;
  };

  // Get the badge class for traditional method
  const getTraditionalBadgeClass = () => {
    const methodName = getTraditionalMethodName()
      .toLowerCase()
      .replace(" ", "-");
    return methodName;
  };

  return (
    <div className="results-page">
      <div className="results-header">
        <button onClick={() => navigate("/")} className="back-btn">
          ← Back to Upload
        </button>
        <h2>Feature Selection Results</h2>
        <div className="method-badges">{getMethodBadges()}</div>
      </div>

      <ResultsOverview results={results} isComparison={isComparison} />

      {isComparison && (
        <>
          <FeatureQualityChart comparison={results.results.comparison} />
          <FeatureOverlapChart comparison={results.results.comparison} />
          <PerformanceComparisonChart comparison={results.results.comparison} />
        </>
      )}

      <div className="features-section">
        {hasGA && (
          <SelectedFeatures
            method={results.results.ga}
            title="Genetic Algorithm Selected Features"
            type="ga"
          />
        )}
        {hasTraditional && (
          <SelectedFeatures
            method={results.results.traditional}
            title={getTraditionalMethodTitle()}
            type={getTraditionalBadgeClass()}
          />
        )}
        {!isComparison && results.results && (
          <SelectedFeatures
            method={results.results}
            title={
              getMainMethod() === "ga"
                ? "Genetic Algorithm Selected Features"
                : getTraditionalMethodTitle()
            }
            type={getMainMethod() === "ga" ? "ga" : getTraditionalBadgeClass()}
          />
        )}
      </div>

      {isComparison && results.results.comparison.recommendation && (
        <div className="recommendation-card">
          <h3>Recommendation</h3>
          <p>{results.results.comparison.recommendation}</p>
        </div>
      )}
    </div>
  );
};

export default ResultsPage;
