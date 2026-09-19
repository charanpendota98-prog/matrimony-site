"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChannelsConsole from "@/components/ChannelsConsole";
import WANumbersConsole from "@/components/WANumbersConsole";

type Me = { role: string; username: string; csrf: string };
type Summary = { profiles: number; pending_profiles: number; open_reports: number; payments?: number; audit?: any[] };

export default function ControlHome() {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    Promise.all([fetch("/api/control/me", { credentials: "include" }), fetch("/api/control/summary", { credentials: "include" })])
      .then(async ([a, b]) => {
        if (a.status === 401) { router.replace("/control/login"); return; }
        if (!a.ok || !b.ok) throw new Error("Unable to load workspace");
        setMe(await a.json()); setSummary(await b.json());
      }).catch(e => setError(e.message));
  }, [router]);
  async function logout() {
    if (!me) return;
    await fetch("/api/control/logout", { method: "POST", credentials: "include", headers: { "X-Control-CSRF": me.csrf } });
    router.replace("/control/login");
  }
  if (!me) return <main className="p-8">{error || "Loading secure workspace…"}</main>;
  const owner = me.role === "owner";
  return <main className="min-h-screen bg-[#fffaf7] p-5 md:p-10">
    <header className="mx-auto flex max-w-6xl items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-widest text-[#7A0C2E]">Private operations</p><h1 className="text-3xl font-bold text-[#0F1F3C]">Workspace</h1><p className="text-sm text-slate-600">Signed in as {me.username} · {me.role}</p></div><button onClick={logout} className="rounded-xl border px-4 py-2 text-sm font-semibold">Sign out</button></header>
    <section className="mx-auto mt-8 grid max-w-6xl gap-4 sm:grid-cols-2 lg:grid-cols-4">{[["Profiles",summary?.profiles],["Pending review",summary?.pending_profiles],["Open reports",summary?.open_reports],...(owner ? [["Payments",summary?.payments]] : [])].map(([label,value])=><div key={String(label)} className="rounded-2xl border bg-white p-5"><p className="text-sm text-slate-500">{label}</p><p className="mt-2 text-3xl font-bold text-[#0F1F3C]">{value ?? "—"}</p></div>)}</section>
    <section className="mx-auto mt-8 max-w-6xl rounded-2xl border bg-white p-6"><h2 className="text-xl font-bold">Work queues</h2><div className="mt-4 flex flex-wrap gap-3"><Link className="rounded-xl bg-[#7A0C2E] px-4 py-3 font-semibold text-white" href="/control/workspace">Moderation workspace</Link>{owner && <><Link className="rounded-xl border px-4 py-3 font-semibold" href="/control/legacy">All operations modules</Link><span className="rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-800">Sensitive exports and money actions remain owner-only.</span></>}</div></section>
    {owner && <section className="mx-auto mt-8 max-w-6xl rounded-2xl border bg-white p-6"><h2 className="text-xl font-bold text-[#0F1F3C]">📡 Channels & marketing distribution</h2><p className="mt-1 text-sm text-slate-600">Add only real Telegram and WhatsApp URLs. Save each channel beside its name; nothing is published until the channel is mapped and active.</p><div className="mt-4"><ChannelsConsole /><WANumbersConsole /></div></section>}
  </main>;
}
