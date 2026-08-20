import React from 'react';
import type { RagResponse } from '~/data/ragData';

interface RagResultCardProps {
  data: RagResponse;
  loading?: boolean;
}

function Tag({ level }: { level: { label: string; className: string } }) {
  return (
    <span className={`text-[10px] font-semibold uppercase tracking-wide rounded-full border px-2 py-0.5 ${level.className}`}>
      {level.label}
    </span>
  );
}

const CITED_REF = /【([A-Za-z0-9]+)】/g;

function confidenceLevel(score: number): { label: string; className: string } {
  if (score >= 0.8) return { label: 'High', className: 'bg-emerald-50 text-emerald-700 border-emerald-100' };
  if (score >= 0.6) return { label: 'Medium', className: 'bg-amber-50 text-amber-700 border-amber-100' };
  return { label: 'Low', className: 'bg-red-50 text-red-700 border-red-100' };
}

function overallConfidence(quality: RagResponse['quality']): number | null {
  const scores = [quality?.citation_accuracy, quality?.faithfulness].filter(
    (v): v is number => typeof v === 'number'
  );
  if (scores.length === 0) return null;
  return Math.min(...scores);
}

function renderCitations(text: string) {
  const parts: React.ReactNode[] = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;
  let key = 0;

  while ((match = CITED_REF.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }
    parts.push(
      <sup
        key={key++}
        className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-blue-100 text-blue-700 text-[10px] font-bold ml-0.5 align-middle cursor-default"
        title={`Citation ${match[1]}`}
      >
        {match[1]}
      </sup>
    );
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }
  return parts;
}

const RagResultCard: React.FC<RagResultCardProps> = ({ data, loading }) => {
  const empty = !data || data.hits.length === 0;

  if (loading) {
    return (
      <div className="bg-white/75 backdrop-blur-md rounded-[20px] border border-white/90 shadow-lg shadow-blue-900/5 p-8 flex flex-col items-center justify-center gap-3 min-h-[180px]">
        <span className="w-8 h-8 rounded-full border-2 border-blue-200 border-t-blue-600 animate-spin" />
        <p className="text-xs text-gray-500 font-medium">Running retrieval + generation…</p>
      </div>
    );
  }

  if (empty && data) {
    return (
      <div className="bg-white/75 backdrop-blur-md rounded-[20px] border border-white/90 shadow-lg shadow-blue-900/5 p-8">
        <div className="flex items-center gap-2 mb-3">
          <span className="w-8 h-8 rounded-full bg-amber-100 text-amber-700 text-sm font-bold flex items-center justify-center">!</span>
          <h3 className="text-sm font-bold text-gray-900">
            {data.disclaimed ? 'Question out of scope' : 'No result'}
          </h3>
        </div>
        <p className="text-[13px] leading-7 text-gray-600 whitespace-pre-wrap">{data.message}</p>
        {data.disclaimed && (
          <div className="mt-4 text-[11px] font-medium text-amber-800 bg-amber-50 border border-amber-100 rounded-xl px-4 py-3">
            {data.reason || 'Only clinical guideline content is answered. Rephrase your question to stay within the scope of the indexed guidelines.'}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bg-white/75 backdrop-blur-md rounded-[20px] border border-white/90 shadow-lg shadow-blue-900/5 p-6 md:p-7 space-y-6">
      {/* Answer */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-full bg-[#111827] text-white text-xs font-bold flex items-center justify-center shadow-sm">AI</span>
            <h3 className="text-sm font-bold text-gray-900">Answer</h3>
          </div>
          <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">
            {data.k} retrieved
          </span>
        </div>
        <p className="text-[15px] leading-7 text-gray-700 whitespace-pre-wrap">{renderCitations(data.message)}</p>
      </div>

      {/* Quality */}
      {data.quality && (data.quality.citation_accuracy != null || data.quality.faithfulness != null) && (
        <div className="space-y-3 border-t border-gray-100 pt-4">
          <div className="flex flex-wrap items-center gap-3 text-[11px] text-gray-500">
            {(() => {
              const overall = overallConfidence(data.quality);
              return overall != null && (
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-gray-600">Confidence:</span>
                  <Tag level={confidenceLevel(overall)} />
                </div>
              );
            })()}
            {data.quality.unsupported_claims && data.quality.unsupported_claims.length > 0 && (
              <div className="space-y-1.5 w-full">
                <span className="font-semibold text-amber-700">Claims without full evidence support:</span>
                {data.quality.unsupported_claims.map((claim, i) => (
                  <p key={i} className="text-[11px] text-amber-700 leading-5">• {claim}</p>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default RagResultCard;