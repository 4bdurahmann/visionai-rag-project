export interface StepItem {
  id: string;
  stepNumber: string;
  title: string;
  description: string;
  icon: string;
}

export const stepsData: StepItem[] = [
  {
    id: '1',
    stepNumber: '1',
    title: 'Find a Specialist',
    description: 'Use filters to choose the best match for your needs.',
    icon: '🛡️',
  },
  {
    id: '2',
    stepNumber: '2',
    title: 'Book an Appointment',
    description: 'Pick a time that works for you — online or in person.',
    icon: '🗓️',
  },
  {
    id: '3',
    stepNumber: '3',
    title: 'Start Your Healing Journey',
    description: 'Talk to your doctor and begin personalized care right away.',
    icon: '✦',
  },
];