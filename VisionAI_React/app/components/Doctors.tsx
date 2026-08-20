import React, { useState } from 'react';
import { doctorsData } from '../data/doctorsData';

const Doctors: React.FC = () => {
  const [activeId, setActiveId] = useState<string>(doctorsData[0].id);

  return (
    <section id="team" className="w-full bg-[#EBF0FA] px-4 py-20">
      <div className="max-w-[1400px] mx-auto px-6">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 gap-6">
          <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight max-w-md leading-tight">
            The Vision AI Team
          </h2>
          <p className="text-gray-500 text-xs md:text-sm max-w-xs font-normal leading-relaxed">
            Two engineers building a cited, verifiable medical Q&A system from retrieval to response.
          </p>
        </div>

        {/* Team Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {doctorsData.map((doc) => {
            const isActive = activeId === doc.id;

            return (
              <div
                key={doc.id}
                onClick={() => setActiveId(doc.id)}
                className="relative rounded-[32px] overflow-hidden bg-[#F2F5FB] border border-white/80 shadow-xs h-[300px] md:h-[340px] flex flex-col justify-end cursor-pointer group transition-all duration-300 hover:shadow-md"
              >
                {/* Background Pattern / Watermark inside card */}
                <div className="absolute inset-0 opacity-10 pointer-events-none flex items-center justify-center">
                  <div className="w-32 h-32 rounded-full border-4 border-gray-400 transform rotate-45" />
                </div>

                {/* Initials Avatar */}
                <div className={`absolute inset-0 w-full h-full flex items-center justify-center transition-all duration-500 ${
                  isActive ? 'scale-105' : 'group-hover:scale-105'
                }`}>
                  <div
                    className={`w-32 h-32 md:w-40 md:h-40 rounded-full flex items-center justify-center text-white text-4xl md:text-5xl font-extrabold shadow-lg border-4 border-white transition-all duration-500 ${
                      isActive
                        ? 'bg-gradient-to-tr from-blue-600 to-indigo-500 scale-110'
                        : 'bg-gradient-to-tr from-gray-300 to-gray-400 grayscale group-hover:grayscale-0'
                    }`}
                  >
                    {doc.initials}
                  </div>
                </div>

                {/* Floating Active Info Card */}
                {isActive && (
                  <div className="relative z-10 m-3 p-4 bg-white/95 backdrop-blur-md rounded-[24px] shadow-lg border border-white/80 text-left animate-fade-in">
                    <h4 className="font-extrabold text-gray-900 text-sm tracking-tight">
                      {doc.name}
                    </h4>
                    <p className="text-[11px] font-medium text-gray-400 mb-3">
                      {doc.role}
                    </p>
                    <span className="inline-flex bg-[#4169E1] hover:bg-blue-700 text-white font-medium text-xs py-2 px-4 rounded-full transition-colors shadow-xs">
                      VISION AI TEAM
                    </span>
                  </div>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
};

export default Doctors