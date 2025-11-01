import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Link, useLocation } from 'react-router-dom';
import ResultsTable from '@/components/ResultsTable';
import StatsTable from '@/components/StatsTable';

// Local types for the result object passed from UploadPage
type FeatureStats = {
  redundancy: string;
  entropy: string;
  diversity: string;
  score: string;
};

type FeatureResult = {
  selected: string[];
  stats?: FeatureStats;
};

type ComparisonResult = {
  ga?: FeatureResult;
  traditional?: FeatureResult;
};

const ResultsPage: React.FC = () => {
  const location = useLocation();
  const state = location.state as { result?: ComparisonResult } | null;
  const result = state?.result;

  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="p-6 space-y-4">
        <h3 className="font-semibold">Results Page</h3>

        {!result && (
          <p className="text-gray-700">No results available. Run feature selection from the Upload page first.</p>
        )}

        {result?.ga && (
          <div className="mb-8">
            <h4 className="font-medium text-lg mb-4">Genetic Algorithm Results</h4>
            <div className="space-y-6">
              <div>
                <h5 className="font-medium mb-2">Selected Features</h5>
                <ResultsTable title="GA Selected Features" features={result.ga.selected} />
              </div>
              {result.ga.stats && (
                <div>
                  <h5 className="font-medium mb-2">Performance Metrics</h5>
                  <StatsTable stats={result.ga.stats} />
                </div>
              )}
            </div>
          </div>
        )}

        {result?.traditional && (
          <div className="mb-8">
            <h4 className="font-medium text-lg mb-4">Traditional Method Results</h4>
            <div className="space-y-6">
              <div>
                <h5 className="font-medium mb-2">Selected Features</h5>
                <ResultsTable title="Traditional Selected Features" features={result.traditional.selected} />
              </div>
              {result.traditional.stats && (
                <div>
                  <h5 className="font-medium mb-2">Performance Metrics</h5>
                  <StatsTable stats={result.traditional.stats} />
                </div>
              )}
            </div>
          </div>
        )}

        <Button asChild><Link to="/">Back to Home</Link></Button>
      </Card>
    </div>
  );
};

export default ResultsPage;
