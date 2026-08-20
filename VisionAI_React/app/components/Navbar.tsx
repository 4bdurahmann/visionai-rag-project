import React from 'react';
import { Link } from 'react-router';
import Logo from './Logo';

const Navbar: React.FC = () => {
  return (
    <div className="w-full bg-[#EBF0FA] px-4 pt-3 pb-0 sticky top-0 z-40">
      <header className="max-w-[1400px] mx-auto bg-white/70 backdrop-blur-md rounded-full px-6 py-3 flex items-center justify-between text-gray-900 shadow-sm border border-white/80">
        
        <Link to="/">
          <Logo />
        </Link>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center gap-8 text-sm font-medium">
          <Link to="/" className="flex items-center gap-1.5 text-blue-600 font-semibold">
            <span className="w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
            Home
          </Link>
          <a href="#how-it-works" className="text-gray-600 hover:text-gray-900 transition-colors">How it works</a>
          <a href="#capabilities" className="text-gray-600 hover:text-gray-900 transition-colors">Capabilities</a>
          <a href="#evaluation" className="text-gray-600 hover:text-gray-900 transition-colors">Evaluation</a>
          <a href="#team" className="text-gray-600 hover:text-gray-900 transition-colors">Team</a>
        </nav>

        {/* CTA Button */}
        <Link
          to="/clinical-rag"
          className="bg-gray-900 hover:bg-black text-white font-semibold px-6 py-2.5 rounded-full text-xs transition-all shadow-sm inline-flex items-center gap-2"
        >
          Ask the AI
          <span aria-hidden>→</span>
        </Link>
      </header>
    </div>
  );
};

export default Navbar