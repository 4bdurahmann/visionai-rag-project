export interface TestimonialItem {
  id: string;
  title: string;
  value: string;
  sublabel: string;
  content: string;
}

export const testimonialsData: TestimonialItem[] = [
  {
    id: '1',
    title: 'Answer coverage',
    value: '13/14',
    sublabel: '92.9%',
    content: 'Clinical questions answered correctly out of a 14-question benchmark set.',
  },
  {
    id: '2',
    title: 'Out-of-scope refusals',
    value: '2/2',
    sublabel: '100%',
    content: 'Non-guideline questions were correctly refused instead of hallucinated.',
  },
  {
    id: '3',
    title: 'Indexed evidence',
    value: '37',
    sublabel: 'chunks',
    content: 'Guideline passages embedded from the USPSTF 2020 CVD-behavioral-counseling recommendation.',
  },
  {
    id: '4',
    title: 'Citation accuracy',
    value: '0.80',
    sublabel: 'sample answer',
    content: 'Citations link to the exact retrieved passages backing each 【N】 marker.',
  },
];