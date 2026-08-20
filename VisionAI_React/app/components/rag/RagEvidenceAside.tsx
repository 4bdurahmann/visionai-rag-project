import React from 'react';
import type { RagResponse } from '~/data/ragData';

interface RagEvidenceAsideProps {
  data: RagResponse;
  loading?: boolean;
}

const RagEvidenceAside: React.FC<RagEvidenceAsideProps> = ({ data, loading }) => {
  const hits = data?.hits ?? [];
  const evidenceCount = hits.length;

  if (loading) {
    return (
      <aside className="bg-white/75 backdrop-blur-md rounded-[20px] border border-white/90 shadow-lg shadow-blue-900/5 p-5 flex flex-col items-center justify-center gap-3 min-h-[200px]">
        <span className="w-6 h-6 rounded-full border-2 border-blue-200 border-t-blue-600 animate-spin" />
        <p className="text-[11px] text-gray-500 font-medium">Retrieving evidence…</p>
      </aside>
    );
  }

  return (
    <aside className="bg-white/75 backdrop-blur-md rounded-[20px] border border-white/90 shadow-lg shadow-blue-900/5 p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white text-xs font-bold flex items-center justify-center shadow-sm">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24" aria-hidden>
              <path d="M6 0h9l5 5v19h-14V0zm8 5V2l3 3h-3z" />
              <path d="M9 9h9v1.5H9V9zm0 3h9v1.5H9V12zm0 3h9v1.5H9V15z" />
            </svg>
          </span>
          <h3 className="text-sm font-bold text-gray-900">Retrieved evidence</h3>
        </div>
        <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">
          {evidenceCount} {evidenceCount === 1 ? 'source' : 'sources'}
        </span>
      </div>

      {hits.length === 0 ? (
        <p className="text-[12px] leading-5 text-gray-500">
          {data?.disclaimed
            ? 'No sources — the question was refused as out of scope.'
            : 'Ask a question to see the retrieved guideline passages.'}
        </p>
      ) : (
        <div className="space-y-3">
          {hits.map((hit, i) => (
            <div key={hit.rank} className="py-3 border-t border-gray-100 first:border-t-0 first:pt-1 space-y-2">
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
              <p className="text-[12px] leading-5 text-gray-600 bg-gray-50/80 border border-gray-100 rounded-lg p-2.5 line-clamp-4">
                {hit.text}
              </p>
            </div>
          ))}

          <div className="pt-1">
            <p className="text-[11px] leading-5 text-gray-400">
              Retrieved via BM25 + PubMedBERT hybrid search.
            </p>
          </div>
        </div>
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