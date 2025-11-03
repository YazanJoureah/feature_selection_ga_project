import React from "react";
import "./Charts.css";

const PerformanceComparisonChart = ({ comparison }) => {
  const performance = comparison.performance_comparison;
  const featureCount = comparison.feature_count_comparison;

  const calculateEfficiencyScore = () => {
    const timeRatio = performance.time_ratio;
    const featureRatio = featureCount.ga / featureCount.traditional;
    return (featureRatio / timeRatio).toFixed(2);
  };

  return (
    <div className="chart-card">
      <h3>Performance & Efficiency Analysis</h3>

      {/* Performance Bars */}
      <div className="performance-bars">
        <div className="performance-bar">
          <div className="performance-bar-label">Genetic Algorithm</div>
          <div className="performance-bar-chart">
            <div
              className="performance-bar-fill ga"
              style={{
                height: `${(performance.execution_time_ga / 15) * 100}%`,
              }}
            ></div>
          </div>
          <div className="performance-value ga">
            {performance.execution_time_ga}s
          </div>
          <div className="metric-difference">Execution Time</div>
        </div>

        <div className="performance-bar">
          <div className="performance-bar-label">Traditional Method</div>
          <div className="performance-bar-chart">
            <div
              className="performance-bar-fill traditional"
              style={{
                height: `${
                  (performance.execution_time_traditional / 15) * 100
                }%`,
              }}
            ></div>
          </div>
          <div className="performance-value traditional">
            {performance.execution_time_traditional}s
          </div>
          <div className="metric-difference">Execution Time</div>
        </div>
      </div>

      {/* Efficiency Metrics */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "1rem",
          marginTop: "2rem",
        }}
      >
        <div className="metric-comparison-card">
          <div className="metric-title">Time Ratio (GA/Trad)</div>
          <div className="metric-value" style={{ color: "#e67e22" }}>
            {performance.time_ratio.toFixed(2)}
          </div>
          <div className="metric-difference">
            {performance.time_ratio > 1 ? "Slower" : "Faster"}
          </div>
        </div>

        <div className="metric-comparison-card">
          <div className="metric-title">Features Selected</div>
          <div className="metric-value ga">{featureCount.ga}</div>
          <div className="metric-value traditional">
            {featureCount.traditional}
          </div>
          <div className="metric-difference">
            Difference: {featureCount.difference}
          </div>
        </div>

        <div className="metric-comparison-card">
          <div className="metric-title">Efficiency Score</div>
          <div className="metric-value" style={{ color: "#27ae60" }}>
            {calculateEfficiencyScore()}
          </div>
          <div className="metric-difference">Higher is better</div>
        </div>
      </div>

      {/* Performance Insights */}
      <div
        style={{
          background: "#e8f4f8",
          padding: "1.5rem",
          borderRadius: "10px",
          marginTop: "1.5rem",
          borderLeft: "4px solid #3498db",
        }}
      >
        <h4 style={{ color: "#2c3e50", marginBottom: "0.5rem" }}>
          Performance Insights
        </h4>
        <p style={{ color: "#7f8c8d", margin: 0, fontSize: "0.9rem" }}>
          {performance.execution_time_ga >
          performance.execution_time_traditional
            ? `Genetic Algorithm takes ${(
                performance.execution_time_ga /
                performance.execution_time_traditional
              ).toFixed(1)}x longer but selects ${
                featureCount.difference
              } fewer features with better quality metrics.`
            : `Genetic Algorithm is faster while selecting ${Math.abs(
                featureCount.difference
              )} fewer features with improved quality metrics.`}
        </p>
      </div>
    </div>
  );
};

export default PerformanceComparisonChart;
