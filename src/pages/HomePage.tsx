import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

const HomePage: React.FC = () => (
  <div className="container mx-auto px-4 py-8">
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
      <div>
        <h1 className="text-3xl font-bold mb-2">Welcome to Feature Selection Tool</h1>
        <p className="text-gray-600 mb-4">
          Compare Genetic Algorithm (GA) and Traditional feature selection methods, run experiments, and download results.
        </p>
        <div className="flex gap-3">
          <Button asChild><Link to="/upload">Upload Dataset</Link></Button>
          <Button variant="outline" asChild><Link to="/compare">Compare Methods</Link></Button>
        </div>
      </div>

      <div>
        <Card>
          <h3 className="font-semibold mb-2">How it works</h3>
          <ol className="list-decimal ml-5 text-gray-700">
            <li>Upload your CSV and select the target column.</li>
            <li>Pick GA, Traditional or Both and adjust settings.</li>
            <li>Run feature selection and view results & comparisons.</li>
          </ol>
        </Card>
      </div>
    </div>
  </div>
);

export default HomePage;
