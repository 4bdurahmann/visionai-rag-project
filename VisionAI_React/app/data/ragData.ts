export interface RagHit {
  rank: number;
  similarity: number;
  grade: string | null;
  section: string;
  page: number;
  org: string;
  text: string;
}
export interface RagQuality {
  citation_accuracy: number
}
export interface RagResponse {
  query: string;
  k: number;
  strategy: string;
  disclaimed: boolean;
  reason: string;
  message: string;
  hits: RagHit[];
  quality: RagQuality
}

export const initialRagData: RagResponse = {
  query: "What does the USPSTF recommend for adults with cardiovascular disease risk factors?",
  k: 5,
  strategy: "hybrid",
  disclaimed: false,
  reason: "none",
  message: "The USPSTF recommends that adults 18 years or older at increased risk of cardiovascular disease (CVD) receive behavioral counseling to promote a healthy diet and physical activity. This recommendation is graded as B. The increased risk is defined as having one or more of the following: hypertension or elevated blood pressure, dyslipidemia, or mixed risk factors such as metabolic syndrome or an estimated 10-year CVD risk of 7.5% or greater.",
  hits: [
    {
      rank: 1,
      similarity: 0.8262,
      grade: "B",
      section: "Figure. Clinician Summary",
      page: 2,
      org: "USPSTF",
      text: "Table from section 'Figure. Clinician Summary'\nWhat does the USPSTF recommend?: For adults 18 years or older at increased risk of cardiovascular disease (CVD): Provide behavioral counseling to promote a healthy diet and physical activity. Grade: B"
    },
    {
      rank: 2,
      similarity: 0.8648,
      grade: null,
      section: "Figure. Clinician Summary",
      page: 2,
      org: "USPSTF",
      text: "To whom does this recommendation apply?: Adults 18 years or older at increased risk of CVD, defined as those with 1 or more of the following..."
    },
    {
      rank: 3,
      similarity: 0.7608,
      grade: "B",
      section: "Summary of Recommendation",
      page: 1,
      org: "USPSTF",
      text: "## Summary of Recommendation\nThe USPSTF recommends offering or referring adults with cardiovascular disease..."
    }
  ], 
  "quality":{
    "citation_accuracy": 0.8
  }
};