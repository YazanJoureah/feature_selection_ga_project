import React from "react";

const FeatureComparison = ({ comparison }) => {
  const featureAnalysis = comparison.feature_analysis;

  return (
    <div className="card">
      <h3>Feature Analysis</h3>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "2rem",
          marginBottom: "2rem",
        }}
      >
        <div>
          <h4>Common Features</h4>
          <ul className="features-list">
            {featureAnalysis.common_features.map((feature, index) => (
              <li key={index} className="feature-item">
                {feature}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4>Overlap: {featureAnalysis.overlap_percentage}%</h4>
          <p>Percentage of features selected by both methods</p>
        </div>
      </div>

      <div
        style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem" }}
      >
        <div>
          <h4>Unique to GA</h4>
          <ul className="features-list">
            {featureAnalysis.unique_to_ga.map((feature, index) => (
              <li key={index} className="feature-item ga">
                {feature}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h4>Unique to Traditional</h4>
          <ul className="features-list">
            {featureAnalysis.unique_to_traditional.map((feature, index) => (
              <li key={index} className="feature-item traditional">
                {feature}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FeatureComparison;
