import { Service, Doctor, Step, Testimonial } from '../types';

export const servicesData: Service[] = [
  { id: '1', number: '01', title: 'Individual Therapy', description: 'Personalized care for your mental well-being with licensed therapists.' },
  { id: '2', number: '02', title: 'Couples & Family Counseling', description: 'Navigate relationship struggles and parenting challenges in a supportive space.' },
  { id: '3', number: '03', title: 'Corporate Wellness Programs', description: 'Mental health solutions, workshops, and resilience programs for teams.' },
  { id: '4', number: '04', title: 'Psychiatric Evaluation', description: 'Professional diagnosis, medication management, and ongoing support.' },
  { id: '5', number: '05', title: 'Online Therapy (Telehealth)', description: 'Book virtual appointments with your preferred therapist from anywhere.' },
  { id: '6', number: '06', title: 'Stress & Burnout Management', description: 'Specialized programs for high-stress professions to regain energy.' },
];

export const doctorsData: Doctor[] = [
  { id: '1', name: 'Dr. Sarah Jenkins', role: 'Psychiatrist', image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=300&q=80' },
  { id: '2', name: 'Kaswara Bader', role: 'Cardiologist', image: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=300&q=80' },
  { id: '3', name: 'Dr. Michael Chen', role: 'Clinical Psychologist', image: 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=300&q=80' },
  { id: '4', name: 'Dr. Emily Watson', role: 'Therapist', image: 'https://images.unsplash.com/photo-1594824813566-78a93272d3d0?auto=format&fit=crop&w=300&q=80' },
];

export const stepsData: Step[] = [
  { stepNumber: '1', title: 'Find a Specialist', description: 'Use filters to choose the best match for your needs.' },
  { stepNumber: '2', title: 'Book an Appointment', description: 'Pick a time that works for you — online or in-person.' },
  { stepNumber: '3', title: 'Start Your Healing Journey', description: 'Talk to your doctor and improve your health right away.' },
];

export const testimonialsData: Testimonial[] = [
  { id: '1', name: 'Robert Fox', role: 'CEO at TechCorp', avatar: 'https://i.pravatar.cc/100?img=12', content: 'Outstanding support! The responsiveness and care from the team made a huge difference.', rating: 5 },
  { id: '2', name: 'Guy Hawkins', role: 'Product Designer', avatar: 'https://i.pravatar.cc/100?img=33', content: 'Seamless booking and top-tier professionals. Highly recommended.', rating: 5 },
  { id: '3', name: 'Jenny Wilson', role: 'Marketing Lead', avatar: 'https://i.pravatar.cc/100?img=47', content: 'The online sessions fit perfectly into my busy schedule. Fantastic experience!', rating: 5 },
  { id: '4', name: 'Kristin Harns', role: 'Operations Manager', avatar: 'https://i.pravatar.cc/100?img=5', content: 'Intuitive platform and compassionate experts who really listen.', rating: 5 },
];