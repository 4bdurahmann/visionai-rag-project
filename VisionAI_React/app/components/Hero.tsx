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

        {/* Top Right Social Media Bar */}
        <div className="absolute top-8 right-8 lg:right-16 z-20 flex items-center gap-2 bg-white/60 backdrop-blur-md p-1.5 rounded-full border border-white/80 shadow-sm">
          <a href="#linkedin" className="w-9 h-9 rounded-full bg-white text-gray-800 font-bold text-xs flex items-center justify-center hover:bg-gray-50 transition-all shadow-xs">
            in
          </a>
          <a href="#instagram" className="w-9 h-9 rounded-full bg-transparent text-gray-600 text-xs flex items-center justify-center hover:bg-white/40 transition-all">
            📷
          </a>
          <a href="#twitter" className="w-9 h-9 rounded-full bg-transparent text-gray-600 text-xs flex items-center justify-center hover:bg-white/40 transition-all">
            𝕏
          </a>
        </div>

        <div className="grid lg:grid-cols-12 gap-8 items-center relative z-10">
          
          {/* Left Content Column */}
          <div className="lg:col-span-7 space-y-6 pt-4">
            
            {/* Tag */}
            <div className="inline-block bg-white/80 backdrop-blur-md px-4 py-1.5 rounded-full border border-gray-100 shadow-2xs">
              <span className="text-gray-700 text-xs font-semibold">
                #1 Best Medical Center in the World
              </span>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 tracking-tight leading-[1.12]">
              We bring professional mental health support.
            </h1>

            {/* Subtitle */}
            <p className="text-gray-600 text-sm md:text-base max-w-lg leading-relaxed font-normal">
              Delivering comprehensive mental health support through our innovative platform that seamlessly connects your teams.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link
                    to="/clinical-rag"
                    className="border border-gray-400/80 hover:bg-white/50 text-gray-900 font-semibold px-6 py-3 rounded-full text-xs transition-all"
                  >
                    Get Started Now
                    </Link>
              <button className="bg-[#111827] hover:bg-black text-white font-medium px-6 py-3 rounded-full text-xs transition-all shadow-md">
                Book Appointment
              </button>
            </div>

            {/* Doctors Avatars Floating Card */}
            <div className="pt-6">
              <div className="bg-white/80 backdrop-blur-xl p-3.5 rounded-3xl inline-flex flex-col gap-2 border border-white/90 shadow-lg shadow-blue-900/5">
                <div className="flex items-center gap-1">
                  <div className="flex -space-x-2">
                    <img className="w-9 h-9 rounded-full border-2 border-white object-cover" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop" alt="Doctor" />
                    <img className="w-9 h-9 rounded-full border-2 border-white object-cover" src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop" alt="Doctor" />
                    <img className="w-9 h-9 rounded-full border-2 border-white object-cover" src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop" alt="Doctor" />
                    <img className="w-9 h-9 rounded-full border-2 border-white object-cover" src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop" alt="Doctor" />
                    <img className="w-9 h-9 rounded-full border-2 border-white object-cover" src="https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=100&auto=format&fit=crop" alt="Doctor" />
                  </div>
                  <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white font-bold text-lg flex items-center justify-center border-2 border-white shadow-xs">
                    +
                  </div>
                </div>
                <p className="text-[11px] font-semibold text-gray-800 px-1 leading-tight">
                  More than 150+ experienced<br />doctors around the world
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
                alt="Doctor smiling"
                className="w-full h-auto object-cover rounded-3xl drop-shadow-xl mix-blend-multiply"
              />

              {/* Floating 24h Service Contact Pill */}
              <div className="absolute bottom-6 -left-4 md:-left-10 z-20 bg-white/80 backdrop-blur-md px-5 py-3 rounded-2xl shadow-xl border border-white/90 flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-500 text-white flex items-center justify-center font-bold text-sm shadow-md">
                  📞
                </div>
                <div>
                  <p className="text-[10px] text-gray-500 font-semibold tracking-wide">24 hour service</p>
                  <p className="text-xs font-extrabold text-gray-900">(302) 555-0107</p>
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