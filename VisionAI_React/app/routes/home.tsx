import ClinicalDashboard from "~/pages/ClinicalDashboard";
import type { Route } from "./+types/home";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "VisionAI Medical RAG — Cited Answers Over Clinical Guidelines" },
    { name: "description", content: "Cited, verifiable Q&A over clinical guidelines with hybrid retrieval, confidence gating, and multi-provider LLMs." },
  ];
}
  
const Home = () => {
  return (
    <main className="min-h-screen bg-white">
      <ClinicalDashboard />
    </main>
  );
}
export default Home