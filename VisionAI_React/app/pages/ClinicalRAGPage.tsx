import React, { useState } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import Footer from '~/components/Footer';
import Navbar from '~/components/Navbar';
import RagEvidenceAside from '~/components/rag/RagEvidenceAside';
import RagResultCard from '~/components/rag/RagResultCard';
import RagSearchBox from '~/components/rag/RagSearchBox';
import { initialRagData, type RagResponse } from '~/data/ragData';

const ClinicalRAGPage: React.FC = () => {
  const [query, setQuery] = useState(initialRagData.query);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<RagResponse>(initialRagData);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) {
      toast.error('Please enter a clinical question');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          k: 5,
          strategy: 'hybrid',
        }),
      });

      if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
      }

      const result: RagResponse = await response.json();
      setData(result);
      toast.success('Query processed successfully!');
    } catch (err: any) {
      console.error('API Error:', err);
      toast.error(err.message || 'Failed to connect to backend server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#EBF0FA] font-sans text-gray-900 selection:bg-blue-100 selection:text-blue-600 flex flex-col justify-between">
      {/* React Hot Toast Component */}
      <Toaster position="top-center" reverseOrder={false} />

      <Navbar />

      <main className="flex-1 w-full max-w-[1440px] mx-auto py-8 px-4 md:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Column 1: Search Box & Result Card (8 Columns) */}
          <div className="lg:col-span-8 space-y-6">
            <RagSearchBox
              query={query}
              setQuery={setQuery}
              onSearch={handleSearch}
              loading={loading}
            />

            <RagResultCard data={data} />
          </div>

          {/* Column 2: Evidence Panel (4 Columns) */}
          <div className="lg:col-span-4 sticky top-6">
            <RagEvidenceAside data={data} />
          </div>

        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ClinicalRAGPage;