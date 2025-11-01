import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import ComparePage from './pages/ComparePage';
import ResultsPage from './pages/ResultsPage';
import AboutPage from './pages/AboutPage';
import Layout from './components/Layout';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="upload" element={<UploadPage />} />
          <Route path="compare" element={<ComparePage />} />
          <Route path="results" element={<ResultsPage />} />
          <Route path="about" element={<AboutPage />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
