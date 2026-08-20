import React from 'react';
import type { RagResponse } from '~/data/ragData';

interface RagEvidenceAsideProps {
  data: RagResponse;
}

const RagEvidenceAside: React.FC<RagEvidenceAsideProps> = ({ data }) => {
  const evidenceCount = Math.min(3, data.hits.length);

  return (
    <aside className="bg-white/70 backdrop-blur-md rounded-2xl border border-white/80 shadow-sm p-5 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900">Evidence panel</h3>
        <span className="text-[11px] font-medium text-gray-500">{evidenceCount} sources</span>
      </div>

      {data.hits.slice(0, 3).map((hit, i) => (
        <div key={hit.rank} className="space-y-1">
          <div className="flex items-center justify-between text-[11px] font-medium">
            <span className="text-gray-700">
              {i === 0 ? 'Top answer' : `Supporting ${i + 1}`}
            </span>
            <span className="text-blue-600">
              {hit.section}
            </span>
          </div>
          <div className="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 rounded-full"
              style={{ width: `${Math.min(100, hit.similarity * 100)}%` }}
            />
          </div>
          <p className="text-[12px] leading-5 text-gray-500">
            {hit.org} · page {hit.page} · similarity {hit.similarity.toFixed(4)}
          </p>
        </div>
      ))}

      {data.disclaimed && (
        <p className="text-[12px] leading-5 text-amber-700 bg-amber-50 border border-amber-100 rounded-xl p-3">
          This question was refused as out of scope. Only clinical guideline content is answered.
        </p>
      )}
    </aside>
  );
};

export default RagEvidenceAside;