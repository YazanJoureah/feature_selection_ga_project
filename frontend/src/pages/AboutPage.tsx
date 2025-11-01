import React from 'react';
import { Card } from '@/components/ui/card';

const AboutPage: React.FC = () => (
  <div className="container mx-auto px-4 py-8">
    <Card className="p-6 space-y-4">
      <h3 className="font-semibold">About this Project</h3>
      <p className="text-gray-700">
        This tool demonstrates a UI for comparing Genetic Algorithm (GA) based feature selection
        with traditional filter/wrapper methods. GA is useful for exploring combinatorial feature subsets,
        while traditional methods are faster and deterministic (Variance Threshold, SelectKBest, RFE, etc.).
      </p>
      <h4 className="font-semibold">References</h4>
      <ul className="list-disc ml-6 text-gray-700">
        <li>Genetic Algorithms for feature selection</li>
        <li>Scikit-learn: SelectKBest, VarianceThreshold, RFE</li>
      </ul>
    </Card>
  </div>
);

export default AboutPage;
