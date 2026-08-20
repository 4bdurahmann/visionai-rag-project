import React from 'react';
import type { RagResponse } from '~/data/ragData';

interface RagEvidenceAsideProps {
  data: RagResponse;
  loading?: boolean;
}

const RagEvidenceAside: React.FC<RagEvidenceAsideProps> = ({ data, loading }) => {
  const hits = data?.hits ?? [];
  const evidenceCount = Math.min(3, hits.length);

  if (loading) {
    return (
      <aside className="bg-white/75 backdrop-blur-md rounded-[28px] border border-white/90 shadow-lg shadow-blue-900/5 p-5 flex flex-col items-center justify-center gap-3 min-h-[200px]">
        <span className="w-6 h-6 rounded-full border-2 border-blue-200 border-t-blue-600 animate-spin" />
        <p className="text-[11px] text-gray-500 font-medium">Analyzing retrieved sources…</p>
      </aside>
    );
  }

  return (
    <aside className="bg-white/75 backdrop-blur-md rounded-[28px] border border-white/90 shadow-lg shadow-blue-900/5 p-5 space-y-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-8 h-8 rounded-full bg-blue-50 text-blue-600 text-sm font-bold flex items-center justify-center">📑</span>
          <h3 className="text-sm font-bold text-gray-900">Evidence panel</h3>
        </div>
        <span className="text-[11px] font-semibold text-gray-400">{evidenceCount} sources</span>
      </div>

      {hits.length === 0 ? (
        <p className="text-[12px] leading-5 text-gray-500">
          {data?.disclaimed
            ? 'No sources — the question was refused as out of scope.'
            : 'Ask a question to see the retrieved guideline passages.'}
        </p>
      ) : (
        <>
          {hits.slice(0, 3).map((hit, i) => (
            <div key={hit.rank} className="space-y-2">
              <div className="flex items-center justify-between text-[11px] font-medium">
                <span className="text-gray-700">
                  {i === 0 ? 'Top answer' : `Supporting ${i + 1}`}
                  {hit.grade && (
                    <span className="ml-2 bg-emerald-50 text-emerald-700 rounded-full px-1.5 py-0.5 text-[10px]">
                      Grade {hit.grade}
                    </span>
                  )}
                </span>
                <span className="text-blue-600 max-w-[45%] truncate">
                  {hit.section ?? 'Guideline'}
                </span>
              </div>
              <div className="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full"
                  style={{ width: `${Math.min(100, hit.similarity * 100)}%` }}
                />
              </div>
              <p className="text-[12px] leading-5 text-gray-500">
                {hit.org ?? 'Guideline'}
                {hit.page != null ? ` · page ${hit.page}` : ''}
                <span className="font-mono text-gray-400"> · {hit.similarity.toFixed(4)}</span>
              </p>
            </div>
          ))}

          <div className="pt-2 border-t border-gray-100">
            <p className="text-[11px] leading-5 text-gray-400">
              Retrieved via BM25 + PubMedBERT hybrid search.
            </p>
          </div>
        </>
      )}

      {data?.disclaimed && (
        <p className="text-[12px] leading-5 text-amber-700 bg-amber-50 border border-amber-100 rounded-xl p-3">
          This question was refused as out of scope. Only indexed clinical guideline content is answered.
        </p>
      )}
    </aside>
  );
};

export default RagEvidenceAside;