import ClinicalRAGPage from "~/pages/ClinicalRAGPage";

export function meta() {
  return [
    { title: "Ask the AI — VisionAI Medical RAG" },
    { name: "description", content: "Ask a clinical question and get a cited, graded answer retrieved from clinical guidelines." },
  ];
}

const RAGRoute = () => {
  return <ClinicalRAGPage />;
};
export default RAGRoute;
