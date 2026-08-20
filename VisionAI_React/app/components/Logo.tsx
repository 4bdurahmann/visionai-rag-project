import React from 'react';

interface LogoProps {
  dark?: boolean;
}

const Logo: React.FC<LogoProps> = ({ dark = false }) => {
  return (
    <div className="flex items-center gap-2 font-bold text-xl tracking-tight text-gray-900">
      <div
        className={`w-7 h-7 rounded-full flex items-center justify-center shadow-xs ${
          dark ? 'bg-white text-[#0B0A1E]' : 'bg-gradient-to-tr from-blue-600 to-indigo-500 text-white'
        }`}
      >
        <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
          <path d="M10.5 4h3v6.5H20v3h-6.5V20h-3v-6.5H4v-3h6.5V4z" />
          <circle cx="17.5" cy="6.5" r="1.6" />
        </svg>
      </div>
      <span className={dark ? 'text-white' : 'text-gray-900'}>VisionAI</span>
      <span className="text-[10px] font-semibold uppercase tracking-widest text-blue-500 py-0.5 px-2 rounded-full bg-blue-50/80 border border-blue-100">
        Med RAG
      </span>
    </div>
  );
};

export default Logo;