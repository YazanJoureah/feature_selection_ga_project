import React, { useState } from 'react';
import FileUploadForm from '@/components/FileUploadForm';
import ResultsTable from '@/components/ResultsTable';
import ComparisonChart from '@/components/ComparisonChart';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { runFeatureSelection } from '@/api/api';

interface ComparisonResult {
  ga: { selected: string[]; stats: { redundancy: string; entropy: string; diversity: string; score: string } };
  traditional: { selected: string[]; stats: { redundancy: string; entropy: string; diversity: string; score: string } };
}

const ComparePage: React.FC = () => {
  const [parsedFile, setParsedFile] = useState<{ file: File; fields: string[] } | null>(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [comparison, setComparison] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleCompare = async () => {
    if (!parsedFile?.file || !targetColumn) return alert('Upload CSV and select target column first.');

    const formData = new FormData();
    formData.append('file', parsedFile.file);
    formData.append('target_column', targetColumn);
    formData.append('run_both', 'true');

    setLoading(true);
    try {
      const res = await runFeatureSelection(formData);
      setComparison(res);
    } catch (e) {
      console.error(e);
      alert('Error running comparison');
    } finally {
      setLoading(false);
    }
  };

  const chartData = comparison
    ? [{ name: 'Selected Count', ga: comparison.ga.selected.length, traditional: comparison.traditional.selected.length }]
    : [];

  return (
    <div className="compare-page">
      <div className="compare-grid">
        <section className="compare-form">
          <Card className="p-6 space-y-4">
            <h3 className="section-title">Upload & Compare</h3>
            <FileUploadForm onParsed={setParsedFile} />

            <label className="field-label">Target column</label>
            <select className="select-field" value={targetColumn} onChange={e => setTargetColumn(e.target.value)}>
              <option value="">-- Choose target column --</option>
              {parsedFile?.fields.map(f => <option key={f} value={f}>{f}</option>)}
            </select>

            <Button className="primary full" onClick={handleCompare} disabled={loading}>
              {loading ? 'Comparing...' : 'Compare Both'}
            </Button>
          </Card>
        </section>

        <section className="compare-results">
          <Card className="p-6">
            <h3 className="section-title">Comparison Results</h3>
            {!comparison && <p className="muted">No comparison yet.</p>}

            {comparison && (
              <div className="results-wrap">
                <div className="chart-wrap">
                  <ComparisonChart data={chartData} />
                </div>
                <div className="tables-grid">
                  <ResultsTable title="GA Selected Features" features={comparison.ga.selected} />
                  <ResultsTable title="Traditional Selected Features" features={comparison.traditional.selected} />
                </div>
              </div>
            )}
          </Card>
        </section>
      </div>
    </div>
  );
};

export default ComparePage;
