import React from 'react';

interface Props {
  stats: {
    redundancy: string;
    entropy: string;
    diversity: string;
    score: string;
  };
}

const StatsTable: React.FC<Props> = ({ stats }) => (
  <div className="mt-4 overflow-x-auto">
    <table className="min-w-full text-sm table-auto border border-gray-200">
      <thead>
        <tr className="bg-gray-100">
          <th className="px-3 py-2">Metric</th>
          <th className="px-3 py-2">Value</th>
        </tr>
      </thead>
      <tbody>
        <tr className="bg-gray-50">
          <td className="px-3 py-2 font-medium">Redundancy</td>
          <td className="px-3 py-2">{stats.redundancy}</td>
        </tr>
        <tr>
          <td className="px-3 py-2 font-medium">Entropy</td>
          <td className="px-3 py-2">{stats.entropy}</td>
        </tr>
        <tr className="bg-gray-50">
          <td className="px-3 py-2 font-medium">Diversity</td>
          <td className="px-3 py-2">{stats.diversity}</td>
        </tr>
        <tr>
          <td className="px-3 py-2 font-medium">Score</td>
          <td className="px-3 py-2">{stats.score}</td>
        </tr>
      </tbody>
    </table>
  </div>
);

export default StatsTable;