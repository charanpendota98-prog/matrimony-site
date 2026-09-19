"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function Workspace() {
  const router = useRouter();
  const [role, setRole] = useState(""); const [csrf, setCsrf] = useState(""); const [error, setError] = useState("");
  useEffect(() => { fetch("/api/control/me", { credentials: "include" }).then(async r => { if (r.status === 401) return router.replace("/control/login"); const d = await r.json(); setRole(d.role); setCsrf(d.csrf); }).catch(() => setError("Unable to load workspace")); }, [router]);
  async function logout() { await fetch("/api/control/logout", { method: "POST", credentials: "include", headers: { "X-Control-CSRF": csrf } }); router.replace("/control/login"); }
  return <main className="min-h-screen bg-[#fffaf7] p-6 md:p-10"><div className="mx-auto max-w-5xl"><div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-[#7A0C2E]">Operations</p><h1 className="text-3xl font-bold">Review workspace</h1><p className="text-sm text-slate-600">Role: {role || "loading"}</p></div><button onClick={logout} className="rounded-xl border px-4 py-2">Sign out</button></div>{error && <p className="mt-6 rounded-xl bg-red-50 p-4 text-red-700">{error}</p>}<div className="mt-8 rounded-2xl border bg-white p-6"><h2 className="text-xl font-bold">Assigned queues</h2><p className="mt-2 text-sm text-slate-600">Use the moderation tools below. Contact details and payment values are never sent to worker sessions.</p><div className="mt-5 grid gap-3 sm:grid-cols-3"><div className="rounded-xl bg-slate-50 p-4"><b>Profile review</b><p className="mt-1 text-xs text-slate-600">Approve or request changes.</p></div><div className="rounded-xl bg-slate-50 p-4"><b>Photo moderation</b><p className="mt-1 text-xs text-slate-600">Review safety queue.</p></div><div className="rounded-xl bg-slate-50 p-4"><b>Support reports</b><p className="mt-1 text-xs text-slate-600">Resolve abuse reports.</p></div></div></div></div></main>;
}
