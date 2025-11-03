import React from "react";

const ResultsOverview = ({ results, isComparison }) => {
  const datasetInfo = results.dataset_info;

  return (
    <div className="card">
      <h3>Dataset Overview</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">{datasetInfo.samples}</div>
          <div className="metric-label">Samples</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{datasetInfo.features}</div>
          <div className="metric-label">Original Features</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {datasetInfo.stats.target_distribution["1"]}
          </div>
          <div className="metric-label">Class 1 Samples</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {datasetInfo.stats.target_distribution["0"]}
          </div>
          <div className="metric-label">Class 0 Samples</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {datasetInfo.stats.avg_feature_correlation.toFixed(3)}
          </div>
          <div className="metric-label">Avg Correlation</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {datasetInfo.stats.max_feature_correlation.toFixed(3)}
          </div>
          <div className="metric-label">Max Correlation</div>
        </div>
      </div>
    </div>
  );
};

export default ResultsOverview;
