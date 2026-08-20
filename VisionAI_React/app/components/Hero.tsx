import React from 'react';
import { Link } from 'react-router';

const Hero: React.FC = () => {
  return (
    <section className="w-full bg-[#EBF0FA] px-4 pb-10 pt-4 overflow-hidden">
      <div className="max-w-[1400px] mx-auto bg-gradient-to-br from-[#F5F8FF] via-[#EEF3FD] to-[#E5EDFB] rounded-[40px] relative px-8 lg:px-16 pt-12 pb-24 border border-white/90 shadow-lg overflow-hidden">
        
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

        {/* Top Right Metrics Badge */}
        <div className="absolute top-8 right-8 lg:right-16 z-20 flex items-center gap-2 bg-white/60 backdrop-blur-md p-1.5 rounded-full border border-white/80 shadow-sm">
          <span className="text-[10px] font-bold text-gray-800 px-2 py-1 rounded-full bg-white">37 chunks</span>
          <span className="text-[10px] font-semibold text-gray-600 px-2 py-1">PubMedBERT · Hybrid RAG</span>
        </div>

        <div className="grid lg:grid-cols-12 gap-8 items-center relative z-10">
          
          {/* Left Content Column */}
          <div className="lg:col-span-7 space-y-6 pt-4">
            
            {/* Tag */}
            <div className="inline-block bg-white/80 backdrop-blur-md px-4 py-1.5 rounded-full border border-gray-100 shadow-sm">
              <span className="text-gray-700 text-xs font-semibold">
                Cited, verifiable medical answers
              </span>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 tracking-tight leading-[1.12]">
              Ask clinical questions.
              <br />
              Get answers with <span className="text-blue-600">evidence</span>.
            </h1>

            {/* Subtitle */}
            <p className="text-gray-600 text-sm md:text-base max-w-lg leading-relaxed font-normal">
              VisionAI Medical RAG retrieves the right passages from clinical
              guidelines, then generates answers with inline citations — graded,
              scored, and defensible on every claim.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link
                to="/clinical-rag"
                className="bg-[#111827] hover:bg-black text-white font-semibold px-6 py-3 rounded-full text-xs transition-all shadow-md inline-flex items-center gap-2"
              >
                Try the Demo
                <span aria-hidden>→</span>
              </Link>
              <a
                href="#how-it-works"
                className="border border-gray-400/80 hover:bg-white/50 text-gray-900 font-semibold px-6 py-3 rounded-full text-xs transition-all"
              >
                How it works
              </a>
            </div>

            {/* Evidence Pill */}
            <div className="pt-6">
              <div className="bg-white/80 backdrop-blur-xl p-4 rounded-3xl inline-flex flex-col gap-2 border border-white/90 shadow-lg shadow-blue-900/5">
                <div className="flex items-center gap-2 text-[11px] font-bold text-gray-800 px-1">
                  <span className="w-6 h-6 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center">✓</span>
                  Sample answer · Grade B recommendation (USPSTF 2020)
                </div>
                <p className="text-[12px] leading-relaxed text-gray-600 max-w-md px-1">
                  "Perform behavioral counseling to promote a healthy diet and
                  physical activity for adults at increased risk of CVD【1】."
                </p>
                <div className="flex items-center gap-3 px-1 pt-1 text-[10px] text-gray-500 font-medium">
                  <span className="px-2 py-0.5 rounded-full bg-blue-50 text-blue-700">Similarity 0.83</span>
                  <span className="px-2 py-0.5 rounded-full bg-amber-50 text-amber-700">Fusion 0.03</span>
                  <span className="px-2 py-0.5 rounded-full bg-purple-50 text-purple-700">Faithful ✓</span>
                </div>
              </div>
            </div>

          </div>

          {/* Right Demo Card Column */}
          <div className="lg:col-span-5 relative flex justify-center lg:justify-end mt-8 lg:mt-0">
            
            {/* Query Result Card */}
            <div className="relative z-10 w-full max-w-[440px] bg-white/85 backdrop-blur-xl rounded-3xl border border-white/90 shadow-2xl overflow-hidden">
              <div className="px-5 py-4 border-b border-gray-100 flex items-center gap-2 bg-white/70">
                <span className="w-2 h-2 rounded-full bg-red-300" />
                <span className="w-2 h-2 rounded-full bg-amber-300" />
                <span className="w-2 h-2 rounded-full bg-emerald-300" />
                <span className="ml-2 text-[11px] text-gray-500 font-medium">visionai · post /query</span>
              </div>

              <div className="p-5 space-y-4">
                <div className="flex items-start gap-2">
                  <div className="w-7 h-7 rounded-full bg-blue-600 text-white text-[10px] font-bold flex items-center justify-center shrink-0">Q</div>
                  <p className="text-[13px] font-semibold text-gray-800 leading-snug">
                    What does the USPSTF recommend for adults with CVD risk factors?
                  </p>
                </div>
                <div className="flex items-start gap-2">
                  <div className="w-7 h-7 rounded-full bg-gray-900 text-white text-[10px] font-bold flex items-center justify-center shrink-0">AI</div>
                  <div className="space-y-2">
                    <p className="text-[12px] leading-relaxed text-gray-700">
                      Offer behavioral counseling to promote a healthy diet and
                      physical activity. <mark className="bg-emerald-100 text-emerald-800 px-1 rounded">Grade B</mark>【1】
                    </p>
                    <p className="text-[12px] leading-relaxed text-gray-700">
                      For adults 18 years or older with 1+ CVD risk factors
                      (hypertension, dyslipidemia, or 10-yr risk ≥7.5%)【2】.
                    </p>
                  </div>
                </div>
                <div className="flex items-center justify-between pt-2 text-[10px] text-gray-500 font-medium border-t border-gray-100">
                  <span>Citation accuracy 0.80</span>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700">Valid answer</span>
                </div>
              </div>
            </div>

            {/* Floating 37-chunks note */}
            <div className="absolute -bottom-4 -left-4 md:-left-10 z-20 bg-white/80 backdrop-blur-md px-5 py-3 rounded-2xl shadow-xl border border-white/90 flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white flex items-center justify-center font-bold text-sm shadow-md">
                📚
              </div>
              <div>
                <p className="text-[10px] text-gray-500 font-semibold tracking-wide">Indexed guidelines</p>
                <p className="text-xs font-extrabold text-gray-900">USPSTF 2020 · 37 chunks</p>
              </div>
            </div>

          </div>

        </div>

      </div>
    </section>
  );
};

export default Hero