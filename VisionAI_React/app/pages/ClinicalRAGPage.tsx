import React, { useState } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import Footer from '~/components/Footer';
import Navbar from '~/components/Navbar';
import RagEvidenceAside from '~/components/rag/RagEvidenceAside';
import RagResultCard from '~/components/rag/RagResultCard';
import RagSearchBox from '~/components/rag/RagSearchBox';
import type { RagResponse } from '~/data/ragData';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';

const EMPTY_DATA: RagResponse = {
  query: '',
  k: 5,
  strategy: 'hybrid',
  disclaimed: false,
  reason: 'none',
  message: '',
  hits: [],
  quality: null,
};

const ClinicalRAGPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);
  const [data, setData] = useState<RagResponse>(EMPTY_DATA);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) {
      toast.error('Please enter a clinical question');
      return;
    }

    setLoading(true);
    setStarted(true);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          k: 5,
          strategy: 'hybrid',
        }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const result: RagResponse = await response.json();
      setData(result);
      toast.success('Query processed successfully!');
    } catch (err: any) {
      console.error('API Error:', err);
      setData({
        ...EMPTY_DATA,
        query,
        disclaimed: true,
        reason: 'backend-unreachable',
        message: `The backend is unreachable (${err.message || 'network error'}). Make sure the FastAPI server is running at ${API_URL}, or set VITE_API_URL to your deployed backend before building.`,
      });
      toast.error('Failed to connect to backend server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#EBF0FA] font-sans text-gray-900 selection:bg-blue-100 selection:text-blue-600 flex flex-col justify-between">
      <Toaster position="top-center" reverseOrder={false} />

      <Navbar />

      <main className="flex-1 w-full max-w-[1440px] mx-auto py-8 px-4 md:px-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 tracking-tight">
            Clinical Question — <span className="text-blue-600">Evidence</span>&nbsp;Answer
          </h1>
          <p className="text-gray-500 text-xs md:text-sm mt-2 font-normal max-w-xl">
            Ask a question about any indexed clinical guideline. The system retrieves the
            most relevant passages, gates weak matches, and generates a cited answer.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Column 1: Search Box & Result Card (8 Columns) */}
          <div className="lg:col-span-8 space-y-6">
            <RagSearchBox
              query={query}
              setQuery={setQuery}
              onSearch={handleSearch}
              loading={loading}
            />

            {!started && !loading ? (
              <div className="bg-white/75 backdrop-blur-md rounded-[28px] border border-white/90 shadow-lg shadow-blue-900/5 p-8 md:p-10 text-center">
                <div className="w-14 h-14 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white flex items-center justify-center mx-auto mb-4 shadow-lg shadow-blue-900/10">
                  <svg className="w-6 h-6 fill-current" viewBox="0 0 24 24" aria-hidden>
                    <path d="M10.5 4h3v6.5H20v3h-6.5V20h-3v-6.5H4v-3h6.5V4z" />
                    <circle cx="17.5" cy="6.5" r="1.6" />
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-gray-900 tracking-tight">
                  Ready when you are
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed max-w-md mx-auto mt-2 font-normal">
                  Type a clinical question above — for example <em>"What does the USPSTF
                  recommend for adults with CVD risk factors?"</em> — and watch the evidence
                  panel populate with the exact guideline passages behind the answer.
                </p>
                <div className="flex flex-wrap items-center justify-center gap-2 mt-5 text-[11px] font-medium text-gray-500">
                  <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700">Cited answer</span>
                  <span className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-700">Quality scores</span>
                  <span className="px-3 py-1 rounded-full bg-purple-50 text-purple-700">Out-of-scope refusal</span>
                </div>
              </div>
            ) : (
              <RagResultCard data={data} loading={loading} />
            )}
          </div>

          {/* Column 2: Evidence Panel (4 Columns) */}
          <div className="lg:col-span-4 sticky top-24">
            <RagEvidenceAside data={data} loading={loading} />
          </div>

        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ClinicalRAGPage;