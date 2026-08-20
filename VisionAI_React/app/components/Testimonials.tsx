import React from 'react';
import { testimonialsData } from '../data/testimonialsData';

const Testimonials: React.FC = () => {
  return (
    <section id="evaluation" className="w-full bg-[#EBF0FA] px-4 py-20">
      <div className="max-w-[1400px] mx-auto px-6">
        
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight leading-tight">
            Evaluation, Not<br />
            Promises
          </h2>
          <p className="text-gray-500 text-xs md:text-sm mt-4 max-w-md mx-auto font-normal leading-relaxed">
            Every capability is measured — retrieval, faithfulness, refusals, and citation integrity.
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {testimonialsData.map((item) => (
            <div
              key={item.id}
              className="bg-white/80 backdrop-blur-md p-6 rounded-[28px] border border-white/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-all duration-300 min-h-[240px]"
            >
              <div>
                {/* Metric Header */}
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-bold text-gray-900 text-sm tracking-tight">
                    {item.title}
                  </h4>
                  <span className="text-[10px] text-gray-400 font-medium uppercase tracking-wide">
                    {item.sublabel}
                  </span>
                </div>

                {/* Big Value */}
                <p className="text-5xl font-extrabold text-gray-900 tracking-tight mb-4 bg-gradient-to-r from-blue-600 to-indigo-500 bg-clip-text text-transparent">
                  {item.value}
                </p>

                {/* Description */}
                <p className="text-xs text-gray-600 leading-relaxed font-normal">
                  {item.content}
                </p>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};

export default Testimonials