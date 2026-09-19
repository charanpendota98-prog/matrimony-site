"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

/** Legacy route: operations are now authenticated through the private control portal. */
export default function LegacyAdminRedirect() {
  const router = useRouter();
  useEffect(() => { router.replace("/control"); }, [router]);
  return <main className="p-8 text-center">Redirecting to the secure operations portal…</main>;
}
