import React from 'react';
import { Link } from 'react-router';
import Logo from './Logo';

const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-[#0B0A1E] text-white pt-12 pb-8 px-4 border-t border-white/5">
      <div className="max-w-[1400px] mx-auto px-6">
        
        {/* Main Navigation Links */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-10 pb-16">
          
          {/* Column 1: Brand & Bio */}
          <div className="lg:col-span-2 space-y-4">
            <Link to="/">
              <Logo dark />
            </Link>
            <p className="text-xs text-[#9492C4] leading-relaxed max-w-xs font-normal">
              VisionAI Medical RAG — retrieval-augmented Q&A over clinical
              guidelines. Every answer is cited, graded, and defensible.
            </p>
            {/* Social / Repo Icons */}
            <div className="flex items-center gap-3 pt-2 text-[#9492C4] text-sm">
              <a href="https://github.com/4bdurahmann/visionai-rag-project" target="_blank" rel="noreferrer" className="hover:text-white transition-colors" aria-label="GitHub">
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
                </svg>
              </a>
              <a href="https://github.com/4bdurahmann/visionai-rag-project" target="_blank" rel="noreferrer" className="hover:text-white transition-colors" aria-label="Repository">
                Source code
              </a>
            </div>
          </div>

          {/* Column 2: Product */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">Product</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li><Link to="/clinical-rag" className="hover:text-white transition-colors">Live demo</Link></li>
              <li><a href="#capabilities" className="hover:text-white transition-colors">Capabilities</a></li>
              <li><a href="#how-it-works" className="hover:text-white transition-colors">How it works</a></li>
              <li><a href="#evaluation" className="hover:text-white transition-colors">Evaluation</a></li>
            </ul>
          </div>

          {/* Column 3: Tech */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">Tech Stack</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li>FastAPI + uvicorn</li>
              <li>PubMedBERT · ChromaDB</li>
              <li>BM25 + RRF hybrid</li>
              <li>React Router · Vite</li>
            </ul>
          </div>

          {/* Column 4: Team */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">Team</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li>Hossam Ibrahim</li>
              <li>Abdulrahman</li>
              <li className="pt-1"><span className="text-[#A5A3D4]">VISION AI TEAM</span></li>
            </ul>
          </div>

          {/* Column 5: Contact */}
          <div className="space-y-3">
            <h4 className="font-bold text-sm text-white mb-2">Project</h4>
            <ul className="space-y-2.5 text-xs text-[#9492C4]">
              <li className="flex items-center gap-2">
                <span>📚</span>
                <span>USPSTF 2020 guideline</span>
              </li>
              <li className="flex items-center gap-2">
                <span>📊</span>
                <span>Eval: 13/14 · 92.9%</span>
              </li>
              <li className="flex items-center gap-2">
                <span>📌</span>
                <span>AI Hackathon 2026</span>
              </li>
            </ul>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-[#9492C4]">
          <p>© 2026 VisionAI. All rights reserved.</p>
          <div className="flex items-center gap-6">
            <a href="#home" className="hover:text-white transition-colors">Back to top</a>
            <a href="https://github.com/4bdurahmann/visionai-rag-project" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">GitHub</a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer