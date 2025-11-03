# Feature Selection Analyzer - Frontend

A modern, responsive React application for comparing feature selection methods including Genetic Algorithms and traditional techniques like RFE, Correlation, Variance Threshold, and SelectKBest.

![Feature Selection Analyzer](https://img.shields.io/badge/React-18.2.0-blue) ![Vite](https://img.shields.io/badge/Vite-5.0.0-purple) ![Axios](https://img.shields.io/badge/Axios-1.6.0-green)

## 🚀 Features

### Core Functionality
- **Multi-Method Feature Selection**: Compare Genetic Algorithm with traditional methods
- **File Upload**: CSV dataset upload with automatic column detection
- **Parameter Configuration**: Customizable parameters for each method
- **Real-time Results**: Interactive visualization of feature selection outcomes
- **Performance Comparison**: Side-by-side comparison of method performance

### Supported Methods
- **Genetic Algorithm (GA)**
  - Population size configuration
  - Generations control
  - Crossover and mutation probability tuning
- **Traditional Methods**
  - Recursive Feature Elimination (RFE)
  - Correlation-based selection
  - Variance Threshold
  - SelectKBest

### Visualization & Analytics
- **Feature Quality Metrics**: Redundancy rate, representation entropy, diversity scores
- **Performance Charts**: Execution time and efficiency comparisons
- **Feature Overlap Analysis**: Venn diagrams and common feature identification
- **Interactive Results**: Dynamic charts and responsive data tables

## 🛠️ Installation

### Prerequisites
- Node.js 16.0 or higher
- npm or yarn package manager

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd feature-selection-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Build for Production
```bash
# Build the application
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
src/
├── components/
│   ├── HomePage.jsx           # File upload and parameter configuration
│   ├── ResultsPage.jsx        # Results display and visualization
│   ├── ResultsOverview.jsx    # Dataset overview and summary
│   ├── FeatureQualityChart.jsx # Quality metrics comparison
│   ├── FeatureOverlapChart.jsx # Feature overlap visualization
│   ├── PerformanceComparisonChart.jsx # Performance metrics
│   ├── SelectedFeatures.jsx   # Selected features display
│   └── LoadingSpinner.jsx     # Loading states
├── context/
│   └── ResultsContext.jsx     # Global state management
├── services/
│   └── api.js                 # API service layer
└── styles/
    ├── App.css               # Global styles
    ├── HomePage.css          # Home page styles
    ├── ResultsPage.css       # Results page styles
    └── Charts.css            # Chart component styles
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=https://feature-selection-ga-project.onrender.com/api
VITE_APP_NAME=Feature Selection Analyzer
```

### API Integration
The application integrates with the Feature Selection API:

- **Base URL**: `https://feature-selection-ga-project.onrender.com/api`
- **Endpoints**:
  - `POST /feature-selection` - Single method feature selection
  - `POST /feature-selection/compare` - Compare multiple methods

## 🎯 Usage

### 1. Upload Dataset
- Click the upload area to select a CSV file
- Supported: CSV files up to 5MB
- Automatic column detection and target selection

### 2. Configure Parameters
#### Genetic Algorithm
- **Population Size**: 10-200 individuals
- **Generations**: 10-200 iterations
- **Crossover Probability**: 0-1
- **Mutation Probability**: 0-1

#### Traditional Methods
- **Method Selection**: RFE, Correlation, Variance Threshold, or SelectKBest
- **Number of Features**: 1-50 features to select
- **Variance Threshold**: 0-1 (for Variance Threshold method)

### 3. Run Analysis
- Select single method or comparison mode
- Click "Run Feature Selection"
- Wait for processing (typically 3-4 minutes)

### 4. Analyze Results
- View feature quality metrics
- Compare method performance
- Examine selected features
- Get recommendations based on analysis

## 📊 Output Metrics

### Feature Quality
- **Redundancy Rate**: Lower values indicate less redundant features
- **Representation Entropy**: Higher values indicate better feature diversity
- **Feature Diversity Score**: Higher values indicate more diverse feature sets

### Performance Metrics
- **Execution Time**: Processing time for each method
- **Feature Reduction**: Percentage reduction from original feature set
- **Efficiency Score**: Combined metric of time and feature quality

## 🎨 Styling & Theming

### Design System
- **Colors**: Gradient themes with purple (#667eea) to pink (#764ba2)
- **Typography**: Inter font family with responsive scaling
- **Components**: Glass morphism effects with backdrop blur
- **Responsive**: Mobile-first design with breakpoints at 768px and 480px

### Customization
Modify CSS variables in `src/index.css`:

```css
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --ga-color: #27ae60;
  --traditional-color: #3498db;
  --card-bg: rgba(255, 255, 255, 0.95);
}
```

## 🔄 State Management

### Context API
The application uses React Context for state management:

```javascript
const {
  results,        // Analysis results
  loading,        // Loading state
  error,          // Error messages
  formParams,     // Form parameters
  updateResults,  // Update results
  setLoadingState // Set loading state
} = useResults();
```

## 📱 Responsive Design

### Breakpoints
- **Desktop**: 1200px+ (Full feature set)
- **Tablet**: 768px - 1199px (Adapted layouts)
- **Mobile**: 480px - 767px (Stacked layouts)
- **Small Mobile**: < 480px (Optimized touch interactions)

### Mobile Features
- Touch-friendly button sizes
- Stacked form layouts
- Optimized chart sizes
- Simplified navigation

## 🚦 Performance Optimizations

### Frontend Optimizations
- **Lazy Loading**: Components load on demand
- **Request Deduplication**: Prevent duplicate API calls
- **Error Boundaries**: Graceful error handling
- **Loading States**: Progressive UI updates

### API Optimizations
- **Request Retry**: Automatic retry with exponential backoff
- **Timeout Handling**: 3-minute timeout with user feedback
- **Progress Indicators**: Real-time processing updates

## 🧪 Testing

### Run Tests
```bash
# Unit tests
npm run test

# Test coverage
npm run test:coverage

# E2E tests (if configured)
npm run test:e2e
```

### Test Coverage
- Component rendering
- User interactions
- API service layer
- Error handling
- Responsive behavior

## 🐛 Troubleshooting

### Common Issues

**File Upload Fails**
- Ensure CSV format with header row
- Check file size (< 5MB)
- Verify internet connection

**Long Processing Times**
- Reduce dataset size for testing
- Lower GA parameters (population/generations)
- Check server status

**Display Issues**
- Clear browser cache
- Check console for errors
- Verify API connectivity

### Debug Mode
Enable debug logging in browser console:

```javascript
localStorage.setItem('debug', 'true')
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Standards
- Use Prettier for code formatting
- Follow React best practices
- Write meaningful commit messages
- Add tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Backend API**: [Feature Selection API Documentation](https://feature-selection-ga-project.onrender.com/docs)
- **Live Demo**: [Coming Soon]
- **Issue Tracker**: [GitHub Issues]
- **Releases**: [GitHub Releases]

## 🙏 Acknowledgments

- React team for the excellent framework
- Vite for fast build tooling
- Chart.js for visualization components
- The machine learning community for feature selection research

---

**Built with ❤️ using React, Vite, and modern web technologies**
