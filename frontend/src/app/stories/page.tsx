import type { Metadata } from "next";
import StoriesClient from "./stories-client";

export const metadata: Metadata = {
  title: "Success Stories — పెళ్లయిన జంటలు",
  description:
    "మనవివాహం ద్వారా కలిసిన జంటలు — real success stories. మీకు కూడా ఇలాంటి సంబంధం కావాలంటే ₹99 సంబంధం, మొదటి 3 FREE.",
};

export default function StoriesPage() {
  return <StoriesClient />;
}
