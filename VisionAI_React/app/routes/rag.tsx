import ClinicalRAGPage from "~/pages/ClinicalRAGPage";

export function meta() {
  return [
    { title: "Clinical RAG System" },
    { name: "description", content: "AI Powered Clinical Assistant" },
  ];
}

const RAGRoute = () => {
  return <ClinicalRAGPage />;
};
export default RAGRoute;
