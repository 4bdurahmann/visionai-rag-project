export interface ServiceItem {
  id: string;
  number: string;
  title: string;
  subtitle: string;
  description: string;
}

export const servicesData: ServiceItem[] = [
  {
    id: '1',
    number: '001',
    title: 'Individual Therapy',
    subtitle: 'Personalized care for your mental well-being',
    description: 'Work one-on-one with licensed therapists to address anxiety, depression, stress, or personal challenges — all in a safe, confidential space.',
  },
  {
    id: '2',
    number: '002',
    title: 'Couples & Family Counseling',
    subtitle: 'Stronger relationships through guided conversations',
    description: 'Navigate relationship struggles, parenting challenges, or family conflicts with structured, supportive sessions.',
  },
  {
    id: '3',
    number: '003',
    title: 'Corporate Wellness Programs',
    subtitle: 'Mental health solutions for modern teams',
    description: "We design and deliver therapy access, workshops, and emotional resilience programs tailored to your company's workforce.",
  },
  {
    id: '4',
    number: '004',
    title: 'Psychiatric Evaluation',
    subtitle: 'Professional diagnosis and treatment plans',
    description: 'Our certified psychiatrists provide assessments, prescribe medication (if needed), and offer ongoing supervision and care.',
  },
  {
    id: '5',
    number: '005',
    title: 'Online Therapy (Telehealth)',
    subtitle: 'Support that fits your schedule',
    description: 'Book virtual appointments with your preferred therapist — from anywhere, on any device. Flexible, private, and secure.',
  },
  {
    id: '6',
    number: '006',
    title: 'Stress & Burnout Management',
    subtitle: 'Reclaim energy and emotional balance',
    description: 'Specialized programs for high-pressure lifestyles — ideal for professionals, students, and caregivers facing burnout.',
  },
];