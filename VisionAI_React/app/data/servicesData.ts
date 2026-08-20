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
    title: 'Cited Answers',
    subtitle: 'Every claim is traceable',
    description: 'Generated answers embed 【N】 markers that map directly to the retrieved guideline passages — read the source behind every fact.',
  },
  {
    id: '2',
    number: '002',
    title: 'Hybrid Retrieval',
    subtitle: 'BM25 + dense vectors',
    description: 'Lexical BM25 and PubMedBERT dense vectors are fused with Reciprocal Rank Fusion so recall stays strong across phrasing and spelling.',
  },
  {
    id: '3',
    number: '003',
    title: 'Confidence Gating',
    subtitle: 'Off-topic questions get refused',
    description: 'Similarity, fusion-score and answer-grade gates filter weak retrievals — the model refuses rather than guessing when it is not sure.',
  },
  {
    id: '4',
    number: '004',
    title: 'Self-Evaluation',
    subtitle: 'Faithfulness & citation accuracy',
    description: 'Each run is scored automatically: does the answer stay faithful to evidence, and are the citations pointing to the right passages?',
  },
  {
    id: '5',
    number: '005',
    title: 'Multi-Provider LLMs',
    subtitle: 'Groq · OpenRouter · Gemini · Qwen · OpenAI',
    description: 'Automatic provider fallback keeps the demo online when a key or API is unavailable — with CPU-only inference for the embedding model.',
  },
  {
    id: '6',
    number: '006',
    title: 'Clinical Benchmark',
    subtitle: '13/14 answered correctly',
    description: 'Internal evaluation over 14 clinical questions scores 92.9% answer coverage, with all out-of-scope questions correctly refused.',
  },
];