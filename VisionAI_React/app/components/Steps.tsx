import React from 'react';
import { Link } from 'react-router';
import { stepsData } from '../data/stepsData';

const Steps: React.FC = () => {
  return (
    <section id="how-it-works" className="w-full bg-gradient-to-b from-[#EBF0FA] via-[#F3E8FF]/30 to-[#EBF0FA] px-4 py-20">
      <div className="max-w-[1400px] mx-auto px-6">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-14 gap-6">
          <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight max-w-md leading-tight">
            How It Works<br />
            From Question to Cited Answer.
          </h2>
          <p className="text-gray-500 text-xs md:text-sm max-w-xs font-normal leading-relaxed">
            A three-stage pipeline that retrieves, scores, and answers with traceable evidence.
          </p>
        </div>

        {/* Steps Grid */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          {stepsData.map((step) => (
            <div
              key={step.id}
              className="relative bg-white/80 backdrop-blur-xl p-8 rounded-[24px] border border-white/90 shadow-xs hover:shadow-md transition-all duration-300 flex flex-col justify-between overflow-hidden group min-h-[260px]"
            >
              {/* Big Faded Step Number on Top Right */}
              <span className="absolute top-2 right-6 text-8xl font-extrabold text-gray-200/50 select-none pointer-events-none group-hover:text-blue-100 transition-colors">
                {step.stepNumber}
              </span>

              {/* Top Icon Pill */}
              <div className="relative z-10 w-10 h-10 rounded-full bg-blue-50/80 border border-blue-100 flex items-center justify-center text-blue-600 text-sm font-bold mb-8 shadow-2xs">
                {step.icon}
              </div>

              {/* Text Content */}
              <div className="relative z-10 space-y-2">
                <h3 className="text-xl font-bold text-gray-900 tracking-tight">
                  {step.title}
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed max-w-[240px]">
                  {step.description}
                </p>
              </div>

              {/* Bottom Link */}
              <div className="relative z-10 pt-6">
                <a
                  href="#capabilities"
                  className="text-xs font-bold text-gray-900 hover:text-blue-600 transition-colors underline underline-offset-4 decoration-gray-300 hover:decoration-blue-600"
                >
                  See capability detail
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Center Bottom Action Button */}
        <div className="flex justify-center">
          <Link
            to="/clinical-rag"
            className="bg-[#4F46E5] hover:bg-indigo-700 text-white font-medium px-8 py-3 rounded-full text-xs transition-all shadow-lg shadow-indigo-200"
          >
            Ask your first question
          </Link>
        </div>

      </div>
    </section>
  );
};

export default Steps