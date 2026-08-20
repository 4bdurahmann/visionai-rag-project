import React from 'react';

interface RagSearchBoxProps {
  query: string;
  setQuery: (q: string) => void;
  onSearch: (e: React.FormEvent) => void;
  loading: boolean;
}

const EXAMPLES = [
  "What does the USPSTF recommend for adults with CVD risk factors?",
  "Who should receive behavioral counseling?",
  "What does the USPSTF recommend for adults with diabetes?"
];

const RagSearchBox: React.FC<RagSearchBoxProps> = ({ query, setQuery, onSearch, loading }) => {
  return (
    <div className="bg-white/75 backdrop-blur-md rounded-[28px] border border-white/90 shadow-lg shadow-blue-900/5 p-6 md:p-7">
      <div className="flex items-center gap-2 mb-4">
        <span className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white text-xs font-bold flex items-center justify-center shadow-sm">
          ✳
        </span>
        <div>
          <h2 className="text-sm font-bold text-gray-900 leading-tight">Ask a clinical question</h2>
          <p className="text-[11px] text-gray-500 font-medium">Hybrid retrieval over indexed clinical guidelines</p>
        </div>
      </div>

      <form onSubmit={onSearch} className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
        <div className="flex-1 relative">
          <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-sm pointer-events-none" aria-hidden>
            🔎
          </span>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. What does the USPSTF recommend for CVD risk factors?"
            className="w-full rounded-full border border-gray-200 bg-white pl-11 pr-5 py-3.5 text-sm text-gray-900 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition-all shadow-xs"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="rounded-full bg-[#111827] hover:bg-black disabled:bg-blue-200 text-white text-sm font-semibold px-7 py-3.5 transition-all shadow-md inline-flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <span className="w-4 h-4 rounded-full border-2 border-white/40 border-t-white animate-spin" aria-hidden />
              Retrieving…
            </>
          ) : (
            <>Ask <span aria-hidden>→</span></>
          )}
        </button>
      </form>

      <div className="flex flex-wrap items-center gap-2 mt-4">
        <span className="text-[11px] text-gray-400 font-medium">Try:</span>
        {EXAMPLES.slice(0, 2).map((example) => (
          <button
            key={example}
            type="button"
            disabled={loading}
            onClick={() => setQuery(example)}
            className="text-[11px] font-medium text-blue-700 bg-blue-50/80 hover:bg-blue-100 border border-blue-100 rounded-full px-3 py-1 transition-colors"
          >
            {example}
          </button>
        ))}
      </div>
    </div>
  );
};

export default RagSearchBox;