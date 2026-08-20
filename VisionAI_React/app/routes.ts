import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),

  route("clinical-rag", "routes/rag.tsx"),
] satisfies RouteConfig;