import React from 'react';
import { testimonialsData } from '../data/testimonialsData';

const Testimonials: React.FC = () => {
  return (
    <section id="testimonials" className="w-full bg-[#EBF0FA] px-4 py-20">
      <div className="max-w-[1400px] mx-auto px-6">
        
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight leading-tight">
            What People Say<br />
            About the Demo
          </h2>
          <p className="text-gray-500 text-xs md:text-sm mt-4 max-w-md mx-auto font-normal leading-relaxed">
            Reaction from reviewers who evaluated the evidence quality and reliability.
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {testimonialsData.map((item) => (
            <div
              key={item.id}
              className="bg-white/80 backdrop-blur-md p-6 rounded-[20px] border border-white/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-all duration-300 min-h-[220px]"
            >
              <div>
                {/* User Info Header */}
                <div className="flex items-center gap-3 mb-4">
                  <img
                    src={item.avatar}
                    alt={item.name}
                    className="w-10 h-10 rounded-full object-cover border border-gray-100"
                  />
                  <div>
                    <h4 className="font-bold text-gray-900 text-xs tracking-tight">
                      {item.name}
                    </h4>
                    <p className="text-[10px] text-gray-400 font-medium">
                      {item.role}
                    </p>
                  </div>
                </div>

                {/* Review Text */}
                <p className="text-xs text-gray-600 leading-relaxed font-normal">
                  {item.content}
                </p>
              </div>

              {/* Star Rating */}
              <div className="pt-4 flex items-center gap-1 text-amber-400 text-sm">
                {Array.from({ length: item.rating }).map((_, i) => (
                  <span key={i}>★</span>
                ))}
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};

export default Testimonials