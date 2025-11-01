import React, { useState } from 'react';
import FileUploadForm from '@/components/FileUploadForm';
import ResultsTable from '@/components/ResultsTable';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { runFeatureSelection } from '@/api/api';

type MethodType = 'ga' | 'traditional' | 'both';

interface FeatureStats {
  redundancy: string;
  entropy: string;
  diversity: string;
  score: string;
}

interface FeatureResult {
  selected: string[];
  stats: FeatureStats;
}

interface ComparisonResult {
  ga?: FeatureResult;
  traditional?: FeatureResult;
}

const UploadPage: React.FC = () => {
  const [parsedFile, setParsedFile] = useState<{ file: File; fields: string[] } | null>(null);
  const [targetColumn, setTargetColumn] = useState<string>('');
  const [method, setMethod] = useState<MethodType>('both');
  const [result, setResult] = useState<ComparisonResult | null>(null);

  // GA options
  const [populationSize, setPopulationSize] = useState(30);
  const [generations, setGenerations] = useState(50);
  const [crossoverProb, setCrossoverProb] = useState(0.8);
  const [mutationProb, setMutationProb] = useState(0.1);

  // Traditional options
  const [traditionalMethod, setTraditionalMethod] = useState('rfe');
  const [varianceThreshold, setVarianceThreshold] = useState(0.01);
  const [nFeatures, setNFeatures] = useState(10);

  const handleRun = async () => {
    if (!parsedFile?.file || !targetColumn) return alert('Upload CSV and choose target column first.');

    const formData = new FormData();
    formData.append('file', parsedFile.file);
    formData.append('target_column', targetColumn);
    formData.append('method', method);

    if (method === 'ga' || method === 'both') {
      formData.append('population_size', populationSize.toString());
      formData.append('generations', generations.toString());
      formData.append('crossover_prob', crossoverProb.toString());
      formData.append('mutation_prob', mutationProb.toString());
    }

    if (method === 'traditional' || method === 'both') {
      formData.append('traditional_method', traditionalMethod);
      formData.append('n_features', nFeatures.toString());
      formData.append('variance_threshold', varianceThreshold.toString());
    }

    try {
      const res = await runFeatureSelection(formData);
      setResult(res);
    } catch (e) {
      console.error(e);
      alert('Error running feature selection');
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-grid">
        <section className="upload-form">
          <Card className="p-6 form-card">
            <h3 className="section-title">Upload & Settings</h3>

            <label className="field-label">CSV file</label>
            <FileUploadForm onParsed={setParsedFile} />

            <label className="field-label">Target column</label>
            <select className="select-field" value={targetColumn} onChange={e => setTargetColumn(e.target.value)}>
              <option value="">-- Choose target column --</option>
              {parsedFile?.fields.map(f => <option key={f} value={f}>{f}</option>)}
            </select>

            <label className="field-label">Method</label>
            <select className="select-field" value={method} onChange={e => setMethod(e.target.value as MethodType)}>
              <option value="ga">Genetic Algorithm (GA)</option>
              <option value="traditional">Traditional</option>
              <option value="both">Both</option>
            </select>

            {(method === 'ga' || method === 'both') && (
              <div className="form-section">
                <label className="field-label">Genetic Algorithm Options</label>
                <div className="field-row">
                  <div>
                    <label className="small-label">Population Size</label>
                    <input type="number" value={populationSize} onChange={e => setPopulationSize(Number(e.target.value))} className="select-field" />
                  </div>
                  <div>
                    <label className="small-label">Generations</label>
                    <input type="number" value={generations} onChange={e => setGenerations(Number(e.target.value))} className="select-field" />
                  </div>
                </div>
                <div className="field-row">
                  <div>
                    <label className="small-label">Crossover Prob.</label>
                    <input type="number" step={0.01} value={crossoverProb} onChange={e => setCrossoverProb(Number(e.target.value))} className="select-field" />
                  </div>
                  <div>
                    <label className="small-label">Mutation Prob.</label>
                    <input type="number" step={0.01} value={mutationProb} onChange={e => setMutationProb(Number(e.target.value))} className="select-field" />
                  </div>
                </div>
              </div>
            )}

            {(method === 'traditional' || method === 'both') && (
              <div className="form-section">
                <label className="field-label">Traditional Options</label>
                <label className="small-label">Method</label>
                <select className="select-field" value={traditionalMethod} onChange={e => setTraditionalMethod(e.target.value)}>
                  <option value="rfe">RFE</option>
                  <option value="variance">Variance Threshold</option>
                  <option value="kbest">SelectKBest</option>
                  <option value="correlation">Correlation</option>
                </select>

                <div className="field-row">
                  <div>
                    <label className="small-label">Variance Threshold</label>
                    <input type="number" step={0.01} value={varianceThreshold} onChange={e => setVarianceThreshold(Number(e.target.value))} className="select-field" />
                  </div>
                  <div>
                    <label className="small-label">n Features</label>
                    <input type="number" value={nFeatures} onChange={e => setNFeatures(Number(e.target.value))} className="select-field" />
                  </div>
                </div>
              </div>
            )}

            <Button className="primary full mt-4" onClick={handleRun}>Run Feature Selection</Button>
          </Card>
        </section>

        <section className="upload-results">
          <Card className="p-6 results-card">
            <h3 className="section-title">Results</h3>
            {!result && <p className="muted">No results yet.</p>}

            {result?.ga && <ResultsTable title="GA Selected Features" features={result.ga.selected} />}
            {result?.traditional && <ResultsTable title="Traditional Selected Features" features={result.traditional.selected} />}
          </Card>
        </section>
      </div>
    </div>
  );
};

export default UploadPage;
