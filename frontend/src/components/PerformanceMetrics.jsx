import React from "react";

const PerformanceMetrics = ({ comparison }) => {
  const performance = comparison.performance_comparison;
  const featureCount = comparison.feature_count_comparison;

  return (
    <div className="card">
      <h3>Performance & Feature Count</h3>

      <div className="metrics-grid">
        <div className="metric-card ga">
          <div className="metric-value">{performance.execution_time_ga}s</div>
          <div className="metric-label">GA Execution Time</div>
        </div>

        <div className="metric-card traditional">
          <div className="metric-value">
            {performance.execution_time_traditional}s
          </div>
          <div className="metric-label">Traditional Execution Time</div>
        </div>

        <div className="metric-card ga">
          <div className="metric-value">{featureCount.ga}</div>
          <div className="metric-label">GA Features Selected</div>
        </div>

        <div className="metric-card traditional">
          <div className="metric-value">{featureCount.traditional}</div>
          <div className="metric-label">Traditional Features Selected</div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceMetrics;
