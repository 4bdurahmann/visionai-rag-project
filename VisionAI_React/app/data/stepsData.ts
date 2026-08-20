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
    title: 'Ask a clinical question',
    description: 'Type any question about clinical guidelines — e.g. "What does the USPSTF recommend for CVD risk factors?"',
    icon: '🔍',
  },
  {
    id: '2',
    stepNumber: '2',
    title: 'Retrieve & score evidence',
    description: 'Hybrid BM25 + PubMedBERT vectors return the most relevant passages, filtered by similarity and fusion gates.',
    icon: '🧩',
  },
  {
    id: '3',
    stepNumber: '3',
    title: 'Answer with citations',
    description: 'A medical LLM writes the answer with 【N】 citations, graded and scored for faithfulness and accuracy.',
    icon: '✦',
  },
];