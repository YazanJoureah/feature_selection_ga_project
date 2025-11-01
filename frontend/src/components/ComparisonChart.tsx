import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface Props {
  data: { name: string; ga: number; traditional: number }[];
}

const ComparisonChart: React.FC<Props> = ({ data }) => (
  <div className="w-full h-64">
    <ResponsiveContainer>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="ga" fill="#6366F1" />
        <Bar dataKey="traditional" fill="#10B981" />
      </BarChart>
    </ResponsiveContainer>
  </div>
);

export default ComparisonChart;
