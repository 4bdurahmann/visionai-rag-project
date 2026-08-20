import ClinicalDashboard from "~/pages/ClinicalDashboard";
import type { Route } from "./+types/home";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "Clinical RAG System" },
    { name: "description", content: "AI Powered Defect Detection System" },
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