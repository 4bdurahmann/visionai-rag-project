import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-[#0B0A1E] text-white pt-12 pb-8 px-4 border-t border-white/5">
      <div className="max-w-[1400px] mx-auto px-6">
        
        {/* Main Navigation Links */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-10 pb-16">
          
          {/* Column 1: Brand & Bio */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-2 font-bold text-xl tracking-tight text-white">
              <div className="w-7 h-7 bg-white text-[#0B0A1E] rounded-full flex items-center justify-center font-black text-xs">
                ✳
              </div>
              <span>MedMe</span>
            </div>
            <p className="text-xs text-[#9492C4] leading-relaxed max-w-xs font-normal">
              We are mental health experienced therapists that are passionate about our goal on empowering you mentally with our wellness journey.
            </p>
            {/* Social Icons */}
            <div className="flex items-center gap-3 pt-2 text-[#9492C4] text-sm">
              <a href="#facebook" className="hover:text-white transition-colors">🌐</a>
              <a href="#instagram" className="hover:text-white transition-colors">📷</a>
              <a href="#twitter" className="hover:text-white transition-colors">𝕏</a>
              <a href="#linkedin" className="hover:text-white transition-colors">in</a>
              <a href="#youtube" className="hover:text-white transition-colors">▶</a>
            </div>
          </div>

          {/* Column 2: About Us */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">About Us</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li><a href="#who-we-are" className="hover:text-white transition-colors">Who we are</a></li>
              <li><a href="#our-impact" className="hover:text-white transition-colors">Our Impact</a></li>
              <li><a href="#businesses" className="hover:text-white transition-colors">For Businesses</a></li>
            </ul>
          </div>

          {/* Column 3: Resources */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">Resources</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li><a href="#blog" className="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#event" className="hover:text-white transition-colors">Event</a></li>
              <li><a href="#case-studies" className="hover:text-white transition-colors">Case Studies</a></li>
              <li><a href="#businesses-resources" className="hover:text-white transition-colors">For Businesses</a></li>
            </ul>
          </div>

          {/* Column 4: Services */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">Services</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li><a href="#children" className="hover:text-white transition-colors">Children Therapy</a></li>
              <li><a href="#couple" className="hover:text-white transition-colors">Couple Therapy</a></li>
              <li><a href="#family" className="hover:text-white transition-colors">Family Counselling</a></li>
              <li><a href="#anxiety" className="hover:text-white transition-colors">Anxiety Disaster</a></li>
              <li><a href="#career" className="hover:text-white transition-colors">Career Counselling</a></li>
              <li><a href="#individual" className="hover:text-white transition-colors">Individual Therapy</a></li>
            </ul>
          </div>

          {/* Column 5: Contact Us */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">Contact Us</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li className="flex items-center gap-2">
                <span>✉</span>
                <a href="mailto:Contact@medme.com" className="hover:text-white transition-colors">Contact@medme.com</a>
              </li>
              <li className="flex items-center gap-2">
                <span>📞</span>
                <span>123456789</span>
              </li>
              <li className="flex items-center gap-2">
                <span>📍</span>
                <span>Toronto Ontario, Canada</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-[#9492C4]">
          <p>© 2026 MedMe. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <a href="#privacy" className="hover:text-white transition-colors">Privacy Policy</a>
            <a href="#terms" className="hover:text-white transition-colors">Terms of Service</a>
            <a href="#cookies" className="hover:text-white transition-colors">Cookies Settings</a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer