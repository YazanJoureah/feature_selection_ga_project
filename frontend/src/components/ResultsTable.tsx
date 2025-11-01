import React from 'react';

interface Props {
  title: string;
  features: string[];
}

const ResultsTable: React.FC<Props> = ({ title, features }) => (
  <div className="mt-4">
    <h4 className="font-semibold mb-2">{title}</h4>
    <div className="overflow-auto">
      <table className="min-w-full text-sm table-auto border border-gray-200">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-3 py-2">#</th>
            <th className="px-3 py-2">Feature</th>
          </tr>
        </thead>
        <tbody>
          {features.map((f, i) => (
            <tr key={f} className={i % 2 === 0 ? 'bg-gray-50' : ''}>
              <td className="px-3 py-2">{i + 1}</td>
              <td className="px-3 py-2">{f}</td>
            </tr>
          ))}
          {features.length === 0 && (
            <tr>
              <td colSpan={2} className="px-3 py-4 text-gray-500">No features selected yet.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  </div>
);

export default ResultsTable;
