import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import HomePage from "./components/HomePage";
import ResultsPage from "./components/ResultsPage";
import { ResultsProvider } from "./context/ResultsContext";
import "./App.css";

function App() {
  return (
    <ResultsProvider>
      <Router>
        <div className="App">
          <header className="app-header">
            <h1>Feature Selection Analyzer</h1>
            <p>Compare Genetic Algorithm vs Traditional Methods</p>
          </header>

          <main className="app-main">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ResultsProvider>
  );
}

export default App;
