import React from 'react';

const Navbar: React.FC = () => {
  return (
    <div className="w-full bg-[#EBF0FA] px-4 pt-3 pb-0">
      <header className="max-w-[1400px] mx-auto bg-white/70 backdrop-blur-md rounded-full px-6 py-3 flex items-center justify-between text-gray-900 shadow-sm border border-white/80">
        
        {/* Logo */}
        <div className="flex items-center gap-2 font-bold text-xl tracking-tight text-gray-900">
          <div className="w-7 h-7 bg-gray-900 text-white rounded-full flex items-center justify-center font-black text-xs">
            ✳
          </div>
          <span>MedMe</span>
        </div>

        {/* Navigation Links */}
        <nav className="hidden lg:flex items-center gap-8 text-sm font-medium">
          <a href="#home" className="flex items-center gap-1.5 text-blue-600 font-semibold">
            <span className="w-1.5 h-1.5 bg-blue-600 rounded-full"></span>
            Home
          </a>
          <a href="#about" className="text-gray-600 hover:text-gray-900 transition-colors">About</a>
          <a href="#services" className="text-gray-600 hover:text-gray-900 transition-colors">Services</a>
          <a href="#doctors" className="text-gray-600 hover:text-gray-900 transition-colors">Doctors</a>
          <a href="#appointments" className="text-gray-600 hover:text-gray-900 transition-colors">Appointments</a>
          <a href="#resources" className="text-gray-600 hover:text-gray-900 transition-colors">Resources</a>
          <a href="#contact" className="text-gray-600 hover:text-gray-900 transition-colors">Contact</a>
        </nav>

        {/* CTA Button */}
        <button className="bg-white hover:bg-gray-50 text-gray-900 font-semibold px-6 py-2.5 rounded-full text-xs transition-all shadow-sm border border-gray-200">
          Book Appointment
        </button>
      </header>
    </div>
  );
};


export default Navbar