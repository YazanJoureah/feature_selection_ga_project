# Feature Selection Analyzer - Genetic Algorithm vs Traditional Methods

![Project Banner](https://img.shields.io/badge/Project-BIA601_Feature_Selection-blue) ![React](https://img.shields.io/badge/Frontend-React_18.2.0-green) ![Flask](https://img.shields.io/badge/Backend-Flask_2.3.3-red) ![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)

A comprehensive full-stack web application for comparing Genetic Algorithm feature selection with traditional statistical methods, developed as part of BIA601 coursework.

**العربية:** [مشروع اختيار الميزات باستخدام الخوارزميات الجينية](#مشروع-اختيار-الميزات-باستخدام-الخوارزميات-الجينية)

## 🎯 Project Overview

This project addresses the challenges of feature selection in large datasets containing hundreds or thousands of features:

- **Difficulty in selecting the most important features**
- **Increased model training time** 
- **Risk of overfitting**
- **Complex model interpretation**

The solution implements **Genetic Algorithms** to find optimal feature subsets that maximize model performance while minimizing the number of features used.

## 🚀 Live Demo

- **Frontend Application**: [Coming Soon]
- **Backend API**: `https://feature-selection-ga-project.onrender.com/api`
- **API Documentation**: `https://feature-selection-ga-project.onrender.com/docs`

## 📋 Project Requirements

### 📅 Timeline
- **Student Delivery Date**: September 3, 2025
- **Receipt Date**: November 10, 2025

### 👥 Team Structure
- Teams of 6-8 students

### 📊 Grading Criteria
- **Code Implementation**: 30 points
- **Correct GA Implementation**: 30 points
- **GitHub Usage**: 10 points
- **Web Interfaces**: 10 points
- **Documentation Report**: 10 points
- **Web Hosting**: 10 points

## 🏗️ System Architecture

### Frontend (React + Vite)
```
feature-selection-frontend/
├── src/
│   ├── components/          # React components
│   ├── context/            # State management
│   ├── services/           # API integration
│   └── styles/            # CSS modules
├── public/                # Static assets
└── configuration/         # Build and env config
```

### Backend (Flask + Python)
```
feature_selection_ga_project/
├── app/
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   └── utils/             # Utilities & helpers
├── config.py             # Configuration
└── app.py               # Application entry
```

## 🛠️ Installation & Setup

### Prerequisites
- **Node.js** 16.0+ (Frontend)
- **Python** 3.8+ (Backend)
- **Git** for version control

### Frontend Setup
```bash
# Clone repository
git clone <repository-url>
cd feature-selection-frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm run dev
```

### Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Start Flask server
python app.py
```

### Docker Deployment (Alternative)
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 📡 API Endpoints

### Core Endpoints
- `POST /api/feature-selection` - Single method analysis
- `POST /api/feature-selection/compare` - Multi-method comparison

### Supported Methods
1. **Genetic Algorithm (GA)**
   - Population size configuration
   - Generations control
   - Crossover/mutation probability tuning

2. **Traditional Methods**
   - Recursive Feature Elimination (RFE)
   - Correlation-based selection
   - Variance Threshold
   - SelectKBest

## 🔧 Configuration

### Frontend Environment Variables
```env
VITE_API_BASE_URL=https://feature-selection-ga-project.onrender.com/api
VITE_APP_NAME=Feature Selection Analyzer
```

### Backend Environment Variables
```env
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=5000
SECRET_KEY=your-secret-key
MAX_UPLOAD_SIZE=52428800
```

## 📊 Feature Selection Metrics

### Quality Metrics
- **Redundancy Rate**: Lower values indicate less feature redundancy
- **Representation Entropy**: Higher values indicate better feature diversity  
- **Feature Diversity Score**: Combined metric balancing redundancy and entropy

### Performance Metrics
- **Execution Time**: Algorithm processing time
- **Feature Reduction**: Percentage reduction from original set
- **Efficiency Score**: Combined performance metric

## 🎨 User Interface

### Key Features
- **File Upload**: CSV dataset upload with automatic column detection
- **Parameter Configuration**: Customizable parameters for each method
- **Real-time Results**: Interactive visualization and comparison
- **Responsive Design**: Mobile-first design with adaptive layouts

### Visualization Components
- Feature quality metrics comparison
- Performance charts and execution times
- Feature overlap analysis (Venn diagrams)
- Selected features display

## 🔬 Algorithm Implementation

### Genetic Algorithm Process
1. **Chromosome Representation**: Binary encoding of feature subsets
2. **Fitness Function**: Model performance with feature count penalty
3. **Selection**: Tournament or roulette wheel selection
4. **Crossover**: Single-point or uniform crossover
5. **Mutation**: Bit-flip mutation with probability control

### Traditional Methods
- **RFE**: Recursive feature elimination with cross-validation
- **Correlation**: Pearson correlation with target variable
- **Variance Threshold**: Remove low-variance features
- **SelectKBest**: Select top k features based on statistical tests

## 📈 Results Analysis

### Comparative Analysis
- Statistical comparison between GA and traditional methods
- Feature overlap identification
- Performance benchmarking
- Method recommendation based on dataset characteristics

### Output Format
```json
{
  "selected_features": ["feature1", "feature2", ...],
  "feature_quality": {
    "redundancy_rate": 0.2345,
    "representation_entropy": 0.8765,
    "feature_diversity_score": 0.6712
  },
  "performance_metrics": {
    "execution_time": 45.23,
    "feature_reduction": "60.0%"
  }
}
```

## 🧪 Testing & Validation

### Test Scenarios
- Breast Cancer Wisconsin Dataset analysis
- GA parameter sensitivity testing
- Traditional method comparisons
- Statistical significance testing

### Running Tests
```bash
# Backend tests
python -m pytest tests/

# Frontend tests
npm run test

# Comprehensive testing
./test_comparisons.sh
```

## 📚 Documentation

### Project Documentation
- **Technical Report**: Complete project documentation
- **API Documentation**: Auto-generated API docs
- **Code Documentation**: Inline comments and docstrings
- **User Guide**: Application usage instructions

### Version Control
- **GitHub Repository**: Complete project history
- **Branch Strategy**: Feature branches with PR reviews
- **Commit Standards**: Conventional commit messages

## 🚀 Deployment

### Frontend Deployment
- **Platform**: Vercel/Netlify
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### Backend Deployment
- **Platform**: Render/Heroku
- **Runtime**: Python 3.8+
- **WSGI Server**: Gunicorn

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/description`
3. Commit changes: `git commit -m 'feat: add new feature'`
4. Push to branch: `git push origin feature/description`
5. Open Pull Request

### Code Standards
- **Frontend**: ESLint + Prettier configuration
- **Backend**: Black code formatter
- **Documentation**: Comprehensive README and comments
- **Testing**: Unit tests for critical functionality

## 🐛 Troubleshooting

### Common Issues
- **File Upload**: Ensure CSV format and correct column names
- **Long Processing**: Reduce dataset size or algorithm parameters
- **API Errors**: Check server status and CORS configuration
- **Display Issues**: Clear browser cache and check console errors

### Debug Mode
```javascript
// Frontend debugging
localStorage.setItem('debug', 'true')

// Backend debugging
export DEBUG=True
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Course Instructor**: Dr. Essam Salman
- **React & Flask Communities** for excellent frameworks
- **Scikit-learn** for machine learning implementations
- **Chart.js** for visualization components
- **Research Community** for feature selection algorithms

---

# مشروع اختيار الميزات باستخدام الخوارزميات الجينية

## 🎯 نظرة عامة على المشروع

يهدف هذا المشروع إلى معالجة تحديات اختيار الميزات في مجموعات البيانات الكبيرة التي تحتوي على المئات أو الآلاف من الميزات:

- **صعوبة في اختيار الميزات الأكثر أهمية**
- **زيادة وقت التدريب للنماذج**
- **احتمال حدوث overfitting**
- **صعوبة تفسير النماذج المعقدة**

يحل المشروع هذه التحديات من خلال تنفيذ **الخوارزميات الجينية** للعثور على مجموعات الميزات المثلى التي تعظيم أداء النموذج مع تقليل عدد الميزات المستخدمة.

## 📋 متطلبات المشروع

### 📅 الجدول الزمني
- **تاريخ التسليم للطلاب**: 3 سبتمبر 2025
- **تاريخ الاستلام**: 10 نوفمبر 2025

### 👥 هيكل الفريق
- فرق مكونة من 6-8 طلاب

### 📊 معايير التصحيح
- **الكود**: 30 نقطة
- **تطبيق الخوارزمية الجينية بطريقة صحيحة**: 30 نقطة
- **استخدام Github**: 10 نقطة
- **واجهات الويب**: 10 نقطة
- **التقرير**: 10 نقطة
- **الاستضافة على الويب**: 10 نقطة

## 🚀 المميزات الرئيسية

### الواجهة الأمامية (Frontend)
- **تحميل البيانات**: رفع ملفات CSV مع الكشف التلقائي عن الأعمدة
- **تكوين المعاملات**: معاملات قابلة للتخصيص لكل طريقة
- **النتائج في الوقت الفعلي**: تصور تفاعلي ومقارنة
- **التصميم المتجاوب**: تصميم mobile-first مع تخطيطات متكيفة

### الواجهة الخلفية (Backend)
- **الخوارزمية الجينية**: مع معاملات قابلة للتخصيص
- **الطرق التقليدية**: RFE، الارتباط، عتبة التباين، SelectKBest
- **مقاييس الجودة**: معدل التكرار، إنتروبيا التمثيل، درجة تنوع الميزات
- **المقارنة الإحصائية**: تحليل مقارن مفصل بين الطرق

## 🛠️ خطوات التنفيذ التفصيلية

1. **فهم البيانات وإعدادها**
   - تحليل مجموعة البيانات
   - تنظيف البيانات ومعالجتها
   - تحديد العمود المستهدف

2. **تصميم تمثيل الكروموسوم**
   - الترميز الثنائي لمجموعات الميزات
   - وظيفة اللياقة (Fitness Function)

3. **تنفيذ الخوارزمية الجينية**
   - التحديد (Selection)
   - التهجين (Crossover)
   - الطفرة (Mutation)

4. **التشغيل والتحليل**
   - تشغيل الخوارزميات
   - تحليل النتائج
   - مقارنة الأداء

5. **المقارنة مع الطرق التقليدية**
   - التحليل الإحصائي
   - تحديد الطريقة المثلى

6. **بناء موقع ويب متكامل**
   - عرض الميزات المثلى
   - نتائج المقارنة مع التقنيات الإحصائية

7. **التوثيق عبر GIT**
   - إدارة الإصدارات
   - توثيق كامل لخطوات المشروع

## 📞 معلومات الاتصال

**المشرف:** د. عصام سلمان  
**المادة:** BIA601  
**القسم:** الذكاء الاصطناعي والأعمال

---

**تم البناء باستخدام ❤️ كجزء من مشروع مقرر BIA601**
