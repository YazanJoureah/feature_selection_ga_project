import React, { useState } from 'react';
import Papa from 'papaparse';

interface Props {
  onParsed: (parsed: { file: File; fields: string[] }) => void;
}

const FileUploadForm: React.FC<Props> = ({ onParsed }) => {
  const [columns, setColumns] = useState<string[]>([]);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;

    Papa.parse(f, {
      header: true,
      preview: 10,
      complete: (res) => {
        if (res.meta.fields) {
          setColumns(res.meta.fields);
          onParsed({ file: f, fields: res.meta.fields });
        }
      },
    });
  };

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium">CSV file</label>
      <input type="file" accept=".csv,text/csv" onChange={handleFile} className="block w-full" />
      {columns.length > 0 && <p className="text-sm text-gray-600">Detected columns: {columns.join(', ')}</p>}
    </div>
  );
};

export default FileUploadForm;
