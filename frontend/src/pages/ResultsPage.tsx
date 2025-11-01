import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Link, useLocation } from 'react-router-dom';
import ResultsTable from '@/components/ResultsTable';

// Local types for the result object passed from UploadPage
type FeatureResult = {
  selected: string[];
  stats?: Record<string, any>;
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
          <div>
            <h4 className="font-medium">GA Selected Features</h4>
            <ResultsTable title="GA Selected Features" features={result.ga.selected} />
          </div>
        )}

        {result?.traditional && (
          <div>
            <h4 className="font-medium">Traditional Selected Features</h4>
            <ResultsTable title="Traditional Selected Features" features={result.traditional.selected} />
          </div>
        )}

        <Button asChild><Link to="/">Back to Home</Link></Button>
      </Card>
    </div>
  );
};

export default ResultsPage;
