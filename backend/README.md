# Feature Selection API - Genetic Algorithm vs Traditional Methods

A comprehensive Flask-based web application for comparing Genetic Algorithm (GA) and traditional feature selection methods on datasets, with specialized testing for breast cancer classification.

## 🚀 Overview

This application provides a RESTful API for feature selection, enabling data scientists and researchers to:

- Apply Genetic Algorithm feature selection with customizable parameters
- Compare GA performance against traditional methods (RFE, Correlation, Variance, SelectKBest)
- Analyze feature quality metrics (redundancy, diversity, entropy)
- Generate statistical comparisons for empirical research

## 🎯 Key Features

- **Genetic Algorithm Feature Selection** with customizable population size, generations, crossover and mutation probabilities
- **Traditional Methods** including RFE, Correlation-based, Variance Threshold, and SelectKBest
- **Comprehensive Metrics** calculating redundancy rate, representation entropy, and feature diversity scores
- **Comparative Analysis** with detailed statistical comparisons between methods
- **RESTful API** with JSON responses for easy integration
- **File Upload Support** for CSV, JSON, and Excel files
- **Cross-Origin Resource Sharing (CORS)** enabled for frontend applications

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd feature_selection_ga_project
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

Create a `.env` file (optional) or use environment variables:

```bash
# Environment
FLASK_ENV=development
DEBUG=True

# Server
HOST=0.0.0.0
PORT=5000

# Security
SECRET_KEY=your-secret-key-here

# File Uploads
MAX_UPLOAD_SIZE=52428800
```

## 🚀 Usage

### Starting the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Using Docker (Alternative)

```bash
docker build -t feature-selection-api .
docker run -p 5000:5000 feature-selection-api
```

## 📡 API Endpoints

### 1. Single Method Feature Selection

**Endpoint:** `POST /api/feature-selection`

**Parameters:**

- `file` (required): Dataset file (CSV, JSON, Excel)
- `target_column` (required): Name of the target variable column
- `method` (optional): `ga` or `traditional` (default: `ga`)
- `run_both` (optional): Boolean to run both methods (default: `false`)

**GA Parameters:**

- `population_size`: Number of individuals in population (default: 30)
- `generations`: Number of generations (default: 50)
- `crossover_prob`: Crossover probability (default: 0.8)
- `mutation_prob`: Mutation probability (default: 0.1)

**Traditional Method Parameters:**

- `traditional_method`: `rfe`, `correlation`, `variance`, or `kbest` (default: `rfe`)
- `n_features`: Number of features to select
- `variance_threshold`: Threshold for variance method (default: 0.01)

### 2. Method Comparison

**Endpoint:** `POST /api/feature-selection/compare`

**Parameters:**

- `file` (required): Dataset file
- `target_column` (required): Target variable column
- `methods` (required): Array of methods to compare (`ga`, `traditional`)
- All GA and traditional parameters supported

## 📊 Example Usage

### 1. GA Feature Selection

```bash
curl -X POST http://localhost:5000/api/feature-selection \
  -F "file=@breast_cancer.csv" \
  -F "target_column=diagnosis" \
  -F "method=ga" \
  -F "population_size=50" \
  -F "generations=100"
```

### 2. Traditional Method (RFE)

```bash
curl -X POST http://localhost:5000/api/feature-selection \
  -F "file=@breast_cancer.csv" \
  -F "target_column=diagnosis" \
  -F "method=traditional" \
  -F "traditional_method=rfe" \
  -F "n_features=15"
```

### 3. Compare GA vs Traditional Methods

```bash
curl -X POST http://localhost:5000/api/feature-selection/compare \
  -F "file=@breast_cancer.csv" \
  -F "target_column=diagnosis" \
  -F "methods=ga" \
  -F "methods=traditional" \
  -F "population_size=50" \
  -F "generations=75" \
  -F "traditional_method=correlation" \
  -F "n_features=15"
```

## 📈 Response Format

### Success Response

```json
{
  "success": true,
  "message": "Feature selection completed successfully using Genetic Algorithm",
  "method_used": "Genetic Algorithm",
  "dataset_info": {
    "samples": 569,
    "features": 30,
    "target_column": "diagnosis",
    "stats": {
      "samples": 569,
      "features": 30,
      "target_distribution": {"0": 357, "1": 212},
      "feature_types": {"numerical": 30, "categorical": 0},
      "memory_usage_mb": 0.13,
      "avg_feature_correlation": 0.3245,
      "max_feature_correlation": 0.9876
    }
  },
  "results": {
    "method": "ga",
    "selected_features": ["radius_mean", "texture_mean", ...],
    "num_features": 12,
    "feature_reduction": "60.0%",
    "total_original_features": 30,
    "feature_quality": {
      "redundancy_rate": 0.2345,
      "representation_entropy": 0.8765,
      "feature_diversity_score": 0.6712
    },
    "execution_time": 45.23
  }
}
```

### Comparison Response

```json
{
  "success": true,
  "comparison": {
    "feature_quality_comparison": {
      "redundancy_rate": {
        "ga": 0.2345,
        "traditional": 0.4567,
        "winner": "GA",
        "improvement": 0.2222
      }
    },
    "performance_comparison": {
      "execution_time_ga": 45.23,
      "execution_time_traditional": 12.34,
      "time_ratio": 0.27
    },
    "recommendation": "GA recommended - 0.2222 lower redundancy and 0.1234 higher entropy"
  }
}
```

## 🏗️ Project Structure

```
feature_selection_ga_project/
├── app/
│   ├── routes/
│   │   └── feature_selection/
│   │       ├── base.py           # Base API class
│   │       ├── individual.py     # Single method endpoint
│   │       └── comparison.py     # Comparison endpoint
│   ├── services/
│   │   ├── ga_service.py         # Genetic Algorithm implementation
│   │   └── traditional_service.py # Traditional methods
│   ├── utils/
│   │   ├── serialization.py      # JSON serialization utilities
│   │   ├── metrics_calculator.py # Feature quality metrics
│   │   ├── results_formatter.py  # Result formatting
│   │   ├── comparison_engine.py  # Method comparison logic
│   │   ├── data_processor.py     # Data processing utilities
│   │   ├── validators.py         # Input validation
│   │   └── error_handlers.py     # Error handling
│   └── __init__.py              # Application factory
├── config.py                    # Configuration settings
├── app.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Application environment (development/production)
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: Flask secret key for security
- `HOST`: Server host address
- `PORT`: Server port

### File Upload Settings

- Maximum file size: 50MB
- Supported formats: CSV, JSON, Excel (.xlsx, .xls)
- Upload directory: `app/uploads/`

## 🧪 Testing Framework

### Manual Testing for Research

The application includes comprehensive testing capabilities for empirical research:

```bash
# Test GA parameter variations
./test_ga_variations.sh

# Test traditional methods
./test_traditional_methods.sh

# Run comprehensive comparisons
./test_comparisons.sh
```

### Key Test Scenarios

1. **GA Parameter Sensitivity**: Population size, generations, crossover/mutation probabilities
2. **Traditional Method Comparison**: RFE, Correlation, Variance, SelectKBest
3. **Statistical Analysis**: Feature quality metrics and performance comparisons

## 📊 Metrics Explained

### Feature Quality Metrics

- **Redundancy Rate**: Average correlation between selected features (lower is better)
- **Representation Entropy**: Diversity of feature importance distribution (higher is better)
- **Feature Diversity Score**: Combined metric balancing redundancy and entropy

### Performance Metrics

- **Execution Time**: Algorithm runtime in seconds
- **Feature Reduction**: Percentage reduction in feature count
- **Method Comparison**: Statistical comparison between approaches

## 🎓 Research Applications

### Ideal For:

- Comparing feature selection algorithms
- Empirical analysis of GA vs traditional methods
- Breast cancer dataset feature selection research
- Parameter optimization studies
- Educational demonstrations of evolutionary algorithms

### Breast Cancer Dataset Specialization

Pre-configured for Wisconsin Breast Cancer Dataset analysis with specialized metrics for medical feature selection.

## 🐛 Troubleshooting

### Common Issues

1. **File Upload Fails**

   - Check file format (CSV, JSON, Excel)
   - Verify file size (< 50MB)
   - Ensure target column exists in dataset

2. **GA Takes Too Long**

   - Reduce population size or generations
   - Use smaller datasets for testing
   - Adjust crossover/mutation probabilities

3. **API Not Responding**
   - Check if Flask server is running
   - Verify port 5000 is available
   - Check application logs for errors

### Debug Mode

Enable debug mode for detailed error information:

```bash
export DEBUG=True
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Scikit-learn for traditional feature selection implementations
- Flask and Flask-RESTful for the web framework
- Pandas and NumPy for data processing
- Breast Cancer Wisconsin Dataset for testing and validation

---
