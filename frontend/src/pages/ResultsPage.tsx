import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

const ResultsPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="p-6 space-y-4">
        <h3 className="font-semibold">Results Page</h3>
        <p className="text-gray-700">
          This page is a detailed view for a specific run. Normally it receives results via props or global store.
          You can add download/export functionality here.
        </p>
        <Button asChild><Link to="/">Back to Home</Link></Button>
      </Card>
    </div>
  );
};

export default ResultsPage;
