export interface RagHit {
  rank: number;
  similarity: number;
  grade: string | null;
  section: string | null;
  page: number | null;
  org: string | null;
  text: string;
}
export interface RagQuality {
  faithfulness?: number | null;
  citation_accuracy?: number | null;
  unsupported_claims?: string[];
  bad_citations?: { claim?: string; citation?: string }[];
}
export interface RagResponse {
  query: string;
  k: number;
  strategy: string;
  disclaimed: boolean;
  reason: string;
  message: string;
  hits: RagHit[];
  quality: RagQuality | null;
  request_id?: string | null;
}

export const EXAMPLE_QUESTION =
  "What does the USPSTF recommend for adults with cardiovascular disease risk factors?";