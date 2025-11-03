import React from "react";
import "./Charts.css";

const FeatureOverlapChart = ({ comparison }) => {
  const featureAnalysis = comparison.feature_analysis;
  const featureCount = comparison.feature_count_comparison;

  const gaFeaturesCount = featureAnalysis.unique_to_ga.length;
  const traditionalFeaturesCount = featureAnalysis.unique_to_traditional.length;
  const commonFeaturesCount = featureAnalysis.common_features.length;
  const totalUniqueFeatures =
    gaFeaturesCount + traditionalFeaturesCount + commonFeaturesCount;

  return (
    <div className="chart-card">
      <h3>Feature Selection Overlap Analysis</h3>

      {/* Venn Diagram */}
      <div className="venn-container">
        <div className="venn-circle ga">
          <div className="venn-content">
            <div style={{ fontSize: "1.5rem", fontWeight: "bold" }}>
              {gaFeaturesCount}
            </div>
            <div style={{ fontSize: "0.8rem" }}>GA Only</div>
          </div>
        </div>

        <div className="venn-overlap">
          <div className="venn-content">
            <div style={{ fontSize: "1.2rem", fontWeight: "bold" }}>
              {commonFeaturesCount}
            </div>
            <div style={{ fontSize: "0.7rem" }}>Common</div>
          </div>
        </div>

        <div className="venn-circle traditional">
          <div className="venn-content">
            <div style={{ fontSize: "1.5rem", fontWeight: "bold" }}>
              {traditionalFeaturesCount}
            </div>
            <div style={{ fontSize: "0.8rem" }}>Traditional Only</div>
          </div>
        </div>
      </div>

      <div className="venn-legend">
        <div className="venn-legend-item">
          <div className="venn-color ga"></div>
          <span>Genetic Algorithm ({gaFeaturesCount})</span>
        </div>
        <div className="venn-legend-item">
          <div className="venn-color overlap"></div>
          <span>Common Features ({commonFeaturesCount})</span>
        </div>
        <div className="venn-legend-item">
          <div className="venn-color traditional"></div>
          <span>Traditional Method ({traditionalFeaturesCount})</span>
        </div>
      </div>

      {/* Overlap Statistics */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "1rem",
          marginTop: "2rem",
          textAlign: "center",
        }}
      >
        <div className="metric-comparison-card">
          <div className="metric-title">Overlap Percentage</div>
          <div className="metric-value" style={{ color: "#9b59b6" }}>
            {featureAnalysis.overlap_percentage}%
          </div>
          <div className="metric-difference">Common features ratio</div>
        </div>

        <div className="metric-comparison-card">
          <div className="metric-title">Total Unique Features</div>
          <div className="metric-value" style={{ color: "#2c3e50" }}>
            {totalUniqueFeatures}
          </div>
          <div className="metric-difference">Across both methods</div>
        </div>

        <div className="metric-comparison-card">
          <div className="metric-title">Feature Reduction</div>
          <div className="metric-value ga">{featureCount.reduction_ga}</div>
          <div className="metric-value traditional">
            {featureCount.reduction_traditional}
          </div>
          <div className="metric-difference">
            From original {featureCount.total_original_features} features
          </div>
        </div>
      </div>

      {/* Feature Lists */}
      <div className="features-comparison">
        <div className="feature-list-container ga">
          <h4>Genetic Algorithm Features ({featureCount.ga} total)</h4>
          <ul className="features-list">
            {featureAnalysis.unique_to_ga.map((feature, index) => (
              <li key={index} className="feature-item ga">
                {feature}
              </li>
            ))}
            {featureAnalysis.common_features.map((feature, index) => (
              <li
                key={`common-${index}`}
                className="feature-item"
                style={{ borderLeftColor: "#9b59b6" }}
              >
                <strong>✓</strong> {feature}
              </li>
            ))}
          </ul>
        </div>

        <div className="feature-list-container traditional">
          <h4>
            Traditional Method Features ({featureCount.traditional} total)
          </h4>
          <ul className="features-list">
            {featureAnalysis.unique_to_traditional.map((feature, index) => (
              <li key={index} className="feature-item traditional">
                {feature}
              </li>
            ))}
            {featureAnalysis.common_features.map((feature, index) => (
              <li
                key={`common-${index}`}
                className="feature-item"
                style={{ borderLeftColor: "#9b59b6" }}
              >
                <strong>✓</strong> {feature}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FeatureOverlapChart;
