import React from 'react';

interface RagSearchBoxProps {
  query: string;
  setQuery: (q: string) => void;
  onSearch: (e: React.FormEvent) => void;
  loading: boolean;
}

const RagSearchBox: React.FC<RagSearchBoxProps> = ({ query, setQuery, onSearch, loading }) => {
  return (
    <div className="bg-white/70 backdrop-blur-md rounded-2xl border border-white/80 shadow-sm p-5">
      <h2 className="text-sm font-semibold text-gray-900 mb-3">Ask a clinical question</h2>
      <form onSubmit={onSearch} className="flex items-center gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. What does the USPSTF recommend for CVD risk factors?"
          className="flex-1 rounded-full border border-gray-200 bg-white px-5 py-3 text-sm text-gray-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white text-sm font-semibold px-6 py-3 transition-all shadow-sm"
        >
          {loading ? 'Searching…' : 'Ask'}
        </button>
      </form>
    </div>
  );
};

export default RagSearchBox;