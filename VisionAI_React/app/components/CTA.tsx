import React from 'react';

const CTA: React.FC = () => {
  return (
    <section className="w-full bg-[#0B0A1E] px-4 py-12">
      <div className="max-w-[1400px] mx-auto bg-[#13112E] rounded-[36px] p-12 md:p-20 relative overflow-hidden flex flex-col items-center justify-center text-center">
        
        {/* Background Star / Cross Decorative Graphic */}
        <div className="absolute right-[-40px] md:right-10 top-1/2 -translate-y-1/2 pointer-events-none opacity-20 text-[#3B387E]">
          <svg className="w-[300px] h-[300px] md:w-[450px] md:h-[450px] fill-current" viewBox="0 0 24 24">
            <path d="M10.5 0h3v10.5H24v3H13.5V24h-3V13.5H0v-3h10.5V0z" />
          </svg>
        </div>

        {/* Top Small Label */}
        <span className="text-[#A5A3D4] text-xs font-medium tracking-wide mb-4">
          (Appointment)
        </span>

        {/* Main Headline */}
        <h2 className="text-3xl md:text-5xl font-extrabold text-white tracking-tight max-w-2xl leading-tight mb-8 relative z-10">
          Seeking Professional Help Is Not a Weakness
        </h2>

        {/* Action Buttons */}
        <div className="flex flex-wrap justify-center items-center gap-4 relative z-10">
          <button className="border border-white/30 hover:bg-white/10 text-white font-medium px-7 py-3 rounded-full text-xs transition-all">
            Get Started Now
          </button>
          <button className="bg-white hover:bg-gray-100 text-[#0B0A1E] font-semibold px-7 py-3 rounded-full text-xs transition-all shadow-md">
            Book Appointment
          </button>
        </div>

      </div>
    </section>
  );
};

export default CTA