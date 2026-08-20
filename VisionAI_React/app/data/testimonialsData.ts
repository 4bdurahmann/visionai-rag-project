export interface TestimonialItem {
  id: string;
  name: string;
  role: string;
  avatar: string;
  content: string;
  rating: number;
}

export const testimonialsData: TestimonialItem[] = [
  {
    id: '1',
    name: 'Dalia Samir',
    role: 'Hackathon Judge',
    avatar: 'https://i.pravatar.cc/100?img=47',
    content: "The cited answers are impressive — every claim points to a specific guideline passage you can verify in seconds.",
    rating: 5,
  },
  {
    id: '2',
    name: 'Ahmed Ali',
    role: 'AI Engineer',
    avatar: 'https://i.pravatar.cc/100?img=33',
    content: "Hybrid retrieval with BM25 and PubMedBERT is well done. The confidence gating stops hallucination before it starts.",
    rating: 5,
  },
  {
    id: '3',
    name: 'Mona Hassan',
    role: 'Healthcare Data Scientist',
    avatar: 'https://i.pravatar.cc/100?img=12',
    content: "Out-of-scope questions are refused cleanly instead of answered with guesswork. That attention to safety is what stands out.",
    rating: 5,
  },
  {
    id: '4',
    name: 'Omar Farouk',
    role: 'Backend Engineer',
    avatar: 'https://i.pravatar.cc/100?img=11',
    content: "Multi-provider fallback is a nice touch — the demo stays responsive even when one LLM API is down.",
    rating: 5,
  },
  {
    id: '5',
    name: 'Sara Ahmed',
    role: 'Product Manager',
    avatar: 'https://i.pravatar.cc/100?img=5',
    content: "Self-evaluation scores for faithfulness and citation accuracy make the results genuinely defensible.",
    rating: 5,
  },
  {
    id: '6',
    name: 'Khaled Mansour',
    role: 'ML Researcher',
    avatar: 'https://i.pravatar.cc/100?img=59',
    content: "A clean end-to-end pipeline from guideline chunking to graded, evidence-backed answers.",
    rating: 5,
  },
];