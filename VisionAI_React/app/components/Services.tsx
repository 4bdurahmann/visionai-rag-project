import React from 'react';
import { servicesData } from '../data/servicesData';

const Services: React.FC = () => {
  return (
    <section id="services" className="w-full bg-[#EBF0FA] px-4 py-16">
      <div className="max-w-[1400px] mx-auto px-6">
        
        {/* Section Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 gap-6">
          <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight max-w-md leading-tight">
            Medical Services You Can Rely On
          </h2>
          <p className="text-gray-500 text-xs md:text-sm max-w-xs font-normal leading-relaxed">
            Comprehensive healthcare solutions designed to keep you and your family healthy at every stage of life.
          </p>
        </div>

        {/* Services Cards Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {servicesData.map((service) => (
            <div
              key={service.id}
              className="bg-[#F8FAFC]/90 backdrop-blur-md p-8 rounded-[28px] border border-white/80 shadow-xs flex flex-col justify-between hover:shadow-md transition-all duration-300 group"
            >
              <div>
                {/* Top Icon & Number Row */}
                <div className="flex justify-between items-center mb-8">
                  <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-gray-900 shadow-xs border border-gray-100 group-hover:scale-105 transition-transform">
                    <svg className="w-4 h-4 fill-current text-gray-900" viewBox="0 0 24 24">
                      <path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z" />
                    </svg>
                  </div>
                  <span className="text-xs font-mono font-medium text-gray-400">
                    {service.number}
                  </span>
                </div>

                {/* Title */}
                <h3 className="text-xl font-bold text-gray-900 mb-2 tracking-tight">
                  {service.title}
                </h3>

                {/* Subtitle */}
                <p className="text-xs font-semibold text-gray-700 mb-4 leading-snug">
                  {service.subtitle}
                </p>

                {/* Detailed Description */}
                <p className="text-xs text-gray-500 leading-relaxed font-normal">
                  {service.description}
                </p>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};

export default Services