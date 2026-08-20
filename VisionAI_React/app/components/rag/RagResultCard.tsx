import React from 'react';
import type { RagResponse } from '~/data/ragData';

interface RagResultCardProps {
  data: RagResponse;
}

const RagResultCard: React.FC<RagResultCardProps> = ({ data }) => {
  return (
    <div className="bg-white/70 backdrop-blur-md rounded-2xl border border-white/80 shadow-sm p-6 space-y-6">
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-gray-900">Answer</h3>
          {data.disclaimed && (
            <span className="text-[11px] font-medium text-amber-700 bg-amber-50 border border-amber-100 rounded-full px-3 py-1">
              Out of scope · {data.reason}
            </span>
          )}
        </div>
        <p className="text-[15px] leading-7 text-gray-700 whitespace-pre-wrap">{data.message}</p>
      </div>

      {data.hits.length > 0 && (
        <div className="space-y-3">
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
            Retrieved evidence ({data.k} · {data.strategy})
          </h4>
          <div className="space-y-2">
            {data.hits.map((hit) => (
              <div
                key={hit.rank}
                className="rounded-xl border border-gray-100 bg-white p-4 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-[11px] font-medium">
                    <span className="bg-blue-50 text-blue-700 rounded-full px-2.5 py-0.5">
                      #{hit.rank}
                    </span>
                    {hit.grade && (
                      <span className="bg-emerald-50 text-emerald-700 rounded-full px-2.5 py-0.5">
                        Grade {hit.grade}
                      </span>
                    )}
                    <span className="text-gray-500">
                      {hit.section} · p.{hit.page} · {hit.org}
                    </span>
                  </div>
                  <span className="text-[11px] text-gray-400 font-mono">
                    {hit.similarity.toFixed(4)}
                  </span>
                </div>
                <p className="text-[13px] leading-6 text-gray-600 line-clamp-3">{hit.text}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {data.quality && (
        <div className="flex items-center gap-2 text-[11px] text-gray-500">
          <span className="font-medium">Citation accuracy:</span>
          <span className="font-mono">
            {typeof data.quality.citation_accuracy === 'number'
              ? data.quality.citation_accuracy.toFixed(2)
              : data.quality.citation_accuracy}
          </span>
        </div>
      )}
    </div>
  );
};

export default RagResultCard;