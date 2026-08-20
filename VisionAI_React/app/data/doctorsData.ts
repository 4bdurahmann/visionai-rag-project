export interface DoctorItem {
  id: string;
  name: string;
  role: string;
  image: string;
  isActive?: boolean;
}

export const doctorsData: DoctorItem[] = [
  {
    id: '1',
    name: 'Dr. Marcus Vance',
    role: 'Psychiatrist',
    image: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: '2',
    name: 'Dr. Elena Rostova',
    role: 'Therapist',
    image: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: '3',
    name: 'Kauwa Qader',
    role: 'Cardiologist',
    image: 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?auto=format&fit=crop&w=600&q=80',
    isActive: true,
  },
  {
    id: '4',
    name: 'Dr. Sarah Jenkins',
    role: 'Neurologist',
    image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=600&q=80',
  },
  {
    id: '5',
    name: 'Dr. Maria Garcia',
    role: 'Pediatrician',
    image: 'https://images.unsplash.com/photo-1651008376811-b90baee60c1f?auto=format&fit=crop&w=600&q=80',
  },
];