import React from 'react';
import { Link } from 'react-router';

const Hero: React.FC = () => {
  return (
    <section className="w-full bg-[#EBF0FA] px-4 pb-10 pt-4 overflow-hidden">
      <div className="max-w-[1400px] mx-auto bg-gradient-to-br from-[#F5F8FF] via-[#EEF3FD] to-[#E5EDFB] rounded-[20px] relative px-8 lg:px-16 pt-12 pb-24 border border-white/90 shadow-lg overflow-hidden">
        
        {/* Circuit Board / Tech Lines Background */}
        <div className="absolute top-0 right-0 w-1/2 h-full pointer-events-none opacity-25">
          <svg className="w-full h-full text-slate-400" viewBox="0 0 500 500" fill="none" stroke="currentColor" strokeWidth="1">
            <path d="M100,50 L200,50 L250,100 L400,100 M250,100 L250,200 L300,250 M150,150 L200,200 L350,200 M300,50 L300,120 M400,150 L450,200" />
            <circle cx="200" cy="50" r="3" fill="currentColor" />
            <circle cx="400" cy="100" r="3" fill="currentColor" />
            <circle cx="350" cy="200" r="3" fill="currentColor" />
            <circle cx="300" cy="250" r="3" fill="currentColor" />
          </svg>
        </div>

        {/* Top Right Social Media Bar */}
        <div className="absolute top-8 right-8 lg:right-16 z-20 flex items-center gap-2 bg-white/60 backdrop-blur-md p-1.5 rounded-full border border-white/80 shadow-sm">
          <a href="https://www.linkedin.com/in/4bdurahmann" target="_blank" rel="noreferrer" className="w-9 h-9 rounded-full bg-white text-gray-800 flex items-center justify-center hover:bg-gray-50 transition-all shadow-xs" aria-label="LinkedIn">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46zM5.34 7.43a2.06 2.06 0 110-4.13 2.06 2.06 0 010 4.13zM7.12 20.45H3.55V9h3.57zM22.22 0H1.78C.8 0 0 .78 0 1.74v20.52c0 .96.8 1.74 1.78 1.74h20.44c.98 0 1.78-.78 1.78-1.74V1.74C24 .78 23.2 0 22.22 0z" />
            </svg>
          </a>
          <a href="https://github.com/4bdurahmann/visionai-rag-project" target="_blank" rel="noreferrer" className="w-9 h-9 rounded-full bg-transparent text-gray-600 flex items-center justify-center hover:bg-white/40 transition-all" aria-label="GitHub">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
          </a>
          <a href="https://github.com/4bdurahmann/visionai-rag-project" target="_blank" rel="noreferrer" className="w-9 h-9 rounded-full bg-transparent text-gray-600 flex items-center justify-center hover:bg-white/40 transition-all" aria-label="Repository">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M10 3a1 1 0 010-2h4a1 1 0 010 2h-4zM7 9a1 1 0 011-1h8a1 1 0 110 2H8a1 1 0 01-1-1zm-1 4a1 1 0 011-1h10a1 1 0 110 2H7a1 1 0 01-1-1zm-1 4a1 1 0 011-1h12a1 1 0 110 2H6a1 1 0 01-1-1zM4 1a1 1 0 011-1h6v20H5a1 1 0 01-1-1V1zm9 19V0h6a1 1 0 011 1v18a1 1 0 01-1 1h-6z" />
            </svg>
          </a>
        </div>

        <div className="grid lg:grid-cols-12 gap-8 items-center relative z-10">
          
          {/* Left Content Column */}
          <div className="lg:col-span-7 space-y-6 pt-4">
            
            {/* Tag */}
            <div className="inline-block bg-white/80 backdrop-blur-md px-4 py-1.5 rounded-full border border-gray-100 shadow-sm">
              <span className="text-gray-700 text-xs font-semibold">
                AI-Powered Medical Q&A
              </span>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 tracking-tight leading-[1.12]">
              Clinical answers with
              <br />
              <span className="text-blue-600">evidence you can trust.</span>
            </h1>

            {/* Subtitle */}
            <p className="text-gray-600 text-sm md:text-base max-w-lg leading-relaxed font-normal">
              Ask a clinical question and get a concise, cited answer retrieved
              straight from official clinical guidelines — graded and scored on
              every claim.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Link
                to="/clinical-rag"
                className="bg-[#111827] hover:bg-black text-white font-medium px-7 py-3 rounded-full text-xs transition-all shadow-md"
              >
                Ask a Question
              </Link>
              <Link
                to="/clinical-rag"
                className="border border-gray-400/80 hover:bg-white/50 text-gray-900 font-semibold px-7 py-3 rounded-full text-xs transition-all"
              >
                Get Started Now
              </Link>
            </div>

            {/* Evidence Adopters Floating Card */}
            <div className="pt-6">
              <div className="bg-white/80 backdrop-blur-xl p-3.5 rounded-2xl inline-flex flex-col gap-2 border border-white/90 shadow-lg shadow-blue-900/5">
                <div className="flex items-center gap-1">
                  <div className="flex -space-x-2">
                    <span className="w-9 h-9 rounded-full border-2 border-white bg-gradient-to-tr from-blue-600 to-indigo-500 text-white text-[10px] font-bold flex items-center justify-center">BM</span>
                    <span className="w-9 h-9 rounded-full border-2 border-white bg-gradient-to-tr from-emerald-500 to-teal-500 text-white text-[10px] font-bold flex items-center justify-center">DB</span>
                    <span className="w-9 h-9 rounded-full border-2 border-white bg-gradient-to-tr from-amber-500 to-orange-500 text-white text-[10px] font-bold flex items-center justify-center">LL</span>
                    <span className="w-9 h-9 rounded-full border-2 border-white bg-gradient-to-tr from-purple-500 to-fuchsia-500 text-white text-[10px] font-bold flex items-center justify-center">RA</span>
                  </div>
                  <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white font-bold text-lg flex items-center justify-center border-2 border-white shadow-xs">
                    +
                  </div>
                </div>
                <p className="text-[11px] font-semibold text-gray-800 px-1 leading-tight">
                  PubMedBERT + BM25 hybrid retrieval<br />
                  over indexed clinical guidelines
                </p>
              </div>
            </div>

          </div>

          {/* Right Doctor Image Column */}
          <div className="lg:col-span-5 relative flex justify-center lg:justify-end mt-8 lg:mt-0">
            
            {/* Doctor Image */}
            <div className="relative z-10 w-full max-w-[440px]">
              <img 
                src="https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=800&q=80" 
                alt="Clinician using the VisionAI medical assistant"
                className="w-full h-auto object-cover rounded-2xl drop-shadow-xl mix-blend-multiply"
              />

              {/* Floating Indexed Guideline Pill */}
              <div className="absolute bottom-6 -left-4 md:-left-10 z-20 bg-white/80 backdrop-blur-md px-5 py-3 rounded-2xl shadow-xl border border-white/90 flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white flex items-center justify-center font-bold text-sm shadow-md">
                  <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24" aria-hidden>
                    <path d="M6 2h12a1 1 0 011 1v18l-2-1.5L15 21V3a1 1 0 011-1H6a2 2 0 00-2 2v16h14V5" />
                  </svg>
                </div>
                <div>
                  <p className="text-[10px] text-gray-500 font-semibold tracking-wide">Indexed guideline</p>
                  <p className="text-xs font-extrabold text-gray-900">USPSTF 2020 · 37 chunks</p>
                </div>
              </div>

            </div>

          </div>

        </div>

      </div>
    </section>
  );
};

export default Hero