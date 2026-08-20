import React from 'react';
import CTA from '~/components/CTA';
import Doctors from '~/components/Doctors';
import Footer from '~/components/Footer';
import Hero from '~/components/Hero';
import Navbar from '~/components/Navbar';
import Services from '~/components/Services';
import Steps from '~/components/Steps';
import Testimonials from '~/components/Testimonials';

const ClinicalDashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-white font-sans text-gray-900 selection:bg-blue-100 selection:text-blue-600">
      <Navbar />
      <main>
        <Hero />
        <Services />
        <Doctors />
        <Steps />
        <Testimonials />
        <CTA />
      </main>
      <Footer />
    </div>
  );
};

export default ClinicalDashboard;