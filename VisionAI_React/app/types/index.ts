export interface Service {
  id: string;
  number: string;
  title: string;
  description: string;
}

export interface Doctor {
  id: string;
  name: string;
  role: string;
  image: string;
}

export interface Step {
  stepNumber: string;
  title: string;
  description: string;
}

export interface Testimonial {
  id: string;
  name: string;
  role: string;
  avatar: string;
  content: string;
  rating: number;
}