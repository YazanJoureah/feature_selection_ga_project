import React from "react";
import "./Charts.css";

const FeatureQualityChart = ({ comparison }) => {
  const metrics = comparison.feature_quality_comparison;

  // Bar chart for direct comparison
  const MetricBarChart = ({
    label,
    gaValue,
    tradValue,
    isLowerBetter = false,
    formatValue = (v) => v.toFixed(3),
  }) => {
    const maxValue = Math.max(gaValue, tradValue) * 1.2; // Add 20% padding
    const gaPercentage = (gaValue / maxValue) * 100;
    const tradPercentage = (tradValue / maxValue) * 100;

    const winner = isLowerBetter
      ? gaValue < tradValue
        ? "ga"
        : "traditional"
      : gaValue > tradValue
      ? "ga"
      : "traditional";

    return (
      <div className="bar-item">
        <div className="bar-label">{label}</div>
        <div className="bar-track">
          <div
            className={`bar-fill ga ${winner === "ga" ? "winner" : ""}`}
            style={{ width: `${gaPercentage}%` }}
          >
            {gaPercentage > 40 && "GA"}
          </div>
        </div>
        <div className="bar-value">{formatValue(gaValue)}</div>

        <div className="bar-track">
          <div
            className={`bar-fill traditional ${
              winner === "traditional" ? "winner" : ""
            }`}
            style={{ width: `${tradPercentage}%` }}
          >
            {tradPercentage > 40 && "Traditional"}
          </div>
        </div>
        <div className="bar-value">{formatValue(tradValue)}</div>
      </div>
    );
  };

  // Radar chart data preparation
  const radarData = {
    metrics: [
      {
        name: "Redundancy",
        ga: 1 - metrics.redundancy_rate.ga,
        trad: 1 - metrics.redundancy_rate.traditional,
      },
      {
        name: "Entropy",
        ga: metrics.representation_entropy.ga * 2,
        trad: metrics.representation_entropy.traditional * 2,
      },
      {
        name: "Diversity",
        ga: metrics.feature_diversity_score.ga * 2,
        trad: metrics.feature_diversity_score.traditional * 2,
      },
      { name: "Efficiency", ga: 0.8, trad: 0.9 }, // Placeholder
      { name: "Stability", ga: 0.7, trad: 0.6 }, // Placeholder
    ],
  };

  return (
    <div className="chart-card">
      <h3>Feature Quality Comprehensive Analysis</h3>

      {/* Bar Chart Comparison */}
      <div className="bar-chart-container">
        <h4>Direct Metric Comparison</h4>
        <div className="bar-chart">
          <MetricBarChart
            label="Redundancy Rate (Lower Better)"
            gaValue={metrics.redundancy_rate.ga}
            tradValue={metrics.redundancy_rate.traditional}
            isLowerBetter={true}
          />
          <MetricBarChart
            label="Representation Entropy (Higher Better)"
            gaValue={metrics.representation_entropy.ga}
            tradValue={metrics.representation_entropy.traditional}
            isLowerBetter={false}
          />
          <MetricBarChart
            label="Feature Diversity (Higher Better)"
            gaValue={metrics.feature_diversity_score.ga}
            tradValue={metrics.feature_diversity_score.traditional}
            isLowerBetter={false}
          />
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-comparison-grid">
        <div
          className={`metric-comparison-card ${
            metrics.redundancy_rate.winner === "GA" ? "winner" : ""
          }`}
        >
          <div className="metric-title">Redundancy Rate</div>
          <div className="metric-value ga">
            {metrics.redundancy_rate.ga.toFixed(3)}
          </div>
          <div className="metric-value traditional">
            {metrics.redundancy_rate.traditional.toFixed(3)}
          </div>
          <div
            className={`metric-difference ${
              metrics.redundancy_rate.improvement > 0 ? "positive" : "negative"
            }`}
          >
            {metrics.redundancy_rate.improvement > 0 ? "↓" : "↑"}{" "}
            {Math.abs(metrics.redundancy_rate.improvement).toFixed(3)}
          </div>
        </div>

        <div
          className={`metric-comparison-card ${
            metrics.representation_entropy.winner === "GA" ? "winner" : ""
          }`}
        >
          <div className="metric-title">Representation Entropy</div>
          <div className="metric-value ga">
            {metrics.representation_entropy.ga.toFixed(3)}
          </div>
          <div className="metric-value traditional">
            {metrics.representation_entropy.traditional.toFixed(3)}
          </div>
          <div
            className={`metric-difference ${
              metrics.representation_entropy.improvement > 0
                ? "positive"
                : "negative"
            }`}
          >
            {metrics.representation_entropy.improvement > 0 ? "↑" : "↓"}{" "}
            {Math.abs(metrics.representation_entropy.improvement).toFixed(3)}
          </div>
        </div>

        <div
          className={`metric-comparison-card ${
            metrics.feature_diversity_score.winner === "GA" ? "winner" : ""
          }`}
        >
          <div className="metric-title">Feature Diversity</div>
          <div className="metric-value ga">
            {metrics.feature_diversity_score.ga.toFixed(3)}
          </div>
          <div className="metric-value traditional">
            {metrics.feature_diversity_score.traditional.toFixed(3)}
          </div>
          <div
            className={`metric-difference ${
              metrics.feature_diversity_score.improvement > 0
                ? "positive"
                : "negative"
            }`}
          >
            {metrics.feature_diversity_score.improvement > 0 ? "↑" : "↓"}{" "}
            {Math.abs(metrics.feature_diversity_score.improvement).toFixed(3)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeatureQualityChart;
