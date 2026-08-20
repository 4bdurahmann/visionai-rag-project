export interface DoctorItem {
  id: string;
  name: string;
  role: string;
  initials: string;
  isActive?: boolean;
}

export const doctorsData: DoctorItem[] = [
  {
    id: '1',
    name: 'Hossam Ibrahim',
    role: 'AI & Backend Engineer',
    initials: 'HI',
    isActive: true,
  },
  {
    id: '2',
    name: 'Abdulrahman',
    role: 'ML & Frontend Engineer',
    initials: 'AB',
  },
];