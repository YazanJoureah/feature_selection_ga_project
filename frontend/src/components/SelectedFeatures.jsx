import React from "react";

const SelectedFeatures = ({ method, title, type }) => {
  return (
    <div className="card">
      <h3>{title}</h3>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">{method.num_features}</div>
          <div className="metric-label">Features Selected</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{method.feature_reduction}</div>
          <div className="metric-label">Feature Reduction</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{method.execution_time}s</div>
          <div className="metric-label">Execution Time</div>
        </div>
      </div>

      <h4 style={{ marginTop: "1.5rem", marginBottom: "1rem" }}>
        Selected Features:
      </h4>
      <ul className="features-list">
        {method.selected_features.map((feature, index) => (
          <li key={index} className={`feature-item ${type}`}>
            {feature}
          </li>
        ))}
      </ul>

      <h4 style={{ marginTop: "1.5rem", marginBottom: "1rem" }}>
        Feature Quality Metrics:
      </h4>
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">
            {method.feature_quality.redundancy_rate.toFixed(3)}
          </div>
          <div className="metric-label">Redundancy Rate</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {method.feature_quality.representation_entropy.toFixed(3)}
          </div>
          <div className="metric-label">Representation Entropy</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {method.feature_quality.feature_diversity_score.toFixed(3)}
          </div>
          <div className="metric-label">Diversity Score</div>
        </div>
      </div>

      {method.parameters_used && (
        <>
          <h4 style={{ marginTop: "1.5rem", marginBottom: "1rem" }}>
            Parameters Used:
          </h4>
          <div className="parameters-grid">
            {Object.entries(method.parameters_used).map(([key, value]) => (
              <div key={key} className="parameter-item">
                <span className="parameter-key">{key}:</span>
                <span className="parameter-value">{value?.toString()}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default SelectedFeatures;
