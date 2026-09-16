import type { Metadata } from "next";
import StoriesClient from "./stories-client";

export const metadata: Metadata = {
  title: "Success Stories — Pelli Ayina Jantalu",
  description:
    "Mana Vivaha dwara kalisina jantalu — real success stories. Meeku kooda ilanti sambandham kavali ante ₹99 ke Sambandham, modati 3 FREE.",
};

export default function StoriesPage() {
  return <StoriesClient />;
}
