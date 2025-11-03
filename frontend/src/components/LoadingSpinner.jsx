import React, { useState, useEffect } from "react";
import "./LoadingSpinner.css";

const LoadingSpinner = ({
  message = "Processing your request...",
  estimatedTime = 45,
}) => {
  const [progress, setProgress] = useState(0);
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        // Slow down progress as it approaches 90%
        if (prev >= 90) return prev + 0.1;
        if (prev >= 70) return prev + 0.5;
        return prev + 1;
      });
    }, 1000);

    const timeInterval = setInterval(() => {
      setElapsedTime((prev) => prev + 1);
    }, 1000);

    return () => {
      clearInterval(progressInterval);
      clearInterval(timeInterval);
    };
  }, []);

  const getStatusMessage = () => {
    if (elapsedTime < 10) return "Initializing feature selection...";
    if (elapsedTime < 25) return "Running genetic algorithm...";
    if (elapsedTime < 40) return "Evaluating feature quality...";
    return "Finalizing results...";
  };

  const getTips = () => {
    const tips = [
      "Feature selection can take 30-60 seconds for optimal results",
      "Larger datasets or more generations will increase processing time",
      "The genetic algorithm explores multiple feature combinations",
      "Results are cached for identical requests",
    ];
    return tips[Math.floor(elapsedTime / 10) % tips.length];
  };

  return (
    <div className="loading-overlay">
      <div className="loading-container">
        <div className="spinner-container">
          <div className="spinner"></div>
          <div className="spinner-ring"></div>
        </div>

        <div className="progress-section">
          <div className="progress-header">
            <h3>{message}</h3>
            <span className="time-elapsed">{elapsedTime}s</span>
          </div>

          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${Math.min(progress, 95)}%` }}
            ></div>
          </div>

          <div className="progress-labels">
            <span>0s</span>
            <span>Estimated: {estimatedTime}s</span>
          </div>
        </div>

        <div className="status-message">
          <p>{getStatusMessage()}</p>
          <div className="tip">💡 {getTips()}</div>
        </div>

        <div className="loading-details">
          <div className="detail-item">
            <span className="detail-label">Status:</span>
            <span className="detail-value">Processing</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Estimated time remaining:</span>
            <span className="detail-value">
              {Math.max(0, estimatedTime - elapsedTime)}s
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
