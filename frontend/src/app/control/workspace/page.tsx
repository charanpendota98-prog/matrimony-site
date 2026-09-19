"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type QueueItem = { tsap_id: string; full_name: string; gender: string; age?: number; district: string; status: string; photo_status: string; created_at: string };

export default function Workspace() {
  const router = useRouter();
  const [role, setRole] = useState(""); const [csrf, setCsrf] = useState(""); const [items, setItems] = useState<QueueItem[]>([]); const [error, setError] = useState(""); const [loading, setLoading] = useState(true);
  useEffect(() => {
    Promise.all([fetch("/api/control/me", { credentials: "include" }), fetch("/api/control/profile-queue?status=pending&limit=50", { credentials: "include" })])
      .then(async ([meRes, queueRes]) => { if (meRes.status === 401) { router.replace("/control/login"); return; } if (!meRes.ok || !queueRes.ok) throw new Error("Unable to load workspace"); const me = await meRes.json(); const queue = await queueRes.json(); setRole(me.role); setCsrf(me.csrf); setItems(queue.items || []); })
      .catch(() => setError("Unable to load workspace"))
      .finally(() => setLoading(false));
  }, [router]);
  async function logout() { await fetch("/api/control/logout", { method: "POST", credentials: "include", headers: { "X-Control-CSRF": csrf } }); router.replace("/control/login"); }
  return <main className="min-h-screen bg-[#fffaf7] p-6 md:p-10"><div className="mx-auto max-w-5xl"><div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-[#7A0C2E]">Operations</p><h1 className="text-3xl font-bold">Review workspace</h1><p className="text-sm text-slate-600">Role: {role || "loading"}</p></div><button onClick={logout} className="rounded-xl border px-4 py-2">Sign out</button></div>{error && <p className="mt-6 rounded-xl bg-red-50 p-4 text-red-700">{error}</p>}<div className="mt-8 rounded-2xl border bg-white p-6"><h2 className="text-xl font-bold">Profile review queue</h2><p className="mt-2 text-sm text-slate-600">Only minimum review fields are shown. Phone numbers, email, payments and IDs are never returned to worker sessions.</p>{loading ? <p className="mt-5 text-sm text-slate-500">Loading queue…</p> : <div className="mt-5 space-y-3">{items.map(item => <div key={item.tsap_id} className="flex flex-wrap items-center gap-3 rounded-xl border p-4"><div className="min-w-[180px] flex-1"><p className="font-semibold">{item.full_name || "Unnamed profile"}</p><p className="text-xs text-slate-500">{item.tsap_id} · {item.gender} · {item.age || "—"} · {item.district || "—"}</p></div><span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-800">{item.status}</span><span className="text-xs text-slate-500">Photo: {item.photo_status}</span></div>)}{!items.length && <p className="text-sm text-slate-500">No pending profiles.</p>}</div>}</div></div></main>;
}
