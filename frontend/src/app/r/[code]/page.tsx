"use client";
import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

export default function ReferralRedirectPage(){
  const params = useParams();
  const router = useRouter();
  const code = params?.code as string;

  useEffect(()=>{
    if(code){
      // Save referral to localStorage for tracking
      localStorage.setItem("tsap_ref_from_link", code);
      // Redirect to register with ref param — auto fill + lock
      router.replace(`/register?ref=${code}`);
    }
  }, [code, router]);

  return (
    <div className="min-h-screen bg-[#FFF8E7] flex items-center justify-center p-4">
      <div className="bg-white rounded-[1.5rem] p-8 card-shadow text-center max-w-md">
        <div className="w-16 h-16 maroon-gradient rounded-full flex items-center justify-center text-white text-2xl mx-auto">🔗</div>
        <h2 className="font-bold text-xl text-[#7A0C2E] mt-4">Referral Link Detected! 🔥</h2>
        <p className="text-sm text-gray-600 mt-2">Code: <span className="font-bold text-[#7A0C2E]">{code}</span> — auto fill + lock avuthundi...</p>
        <div className="mt-4 bg-[#FFF8E7] rounded-xl p-3 text-xs text-left">
          <div className="font-bold">Smart Lock Logic:</div>
          <div className="mt-1">• Link: tsapmatrimony.com/r/{code} → /register?ref={code}</div>
          <div>• Register form lo referral auto fill + 🔒 lock</div>
          <div>• Message: "Lakshmi aunty dwara vacharu — trusted! — 1 extra credit FREE!"</div>
          <div>• Referrer ki commission guarantee — no fraud</div>
        </div>
        <div className="mt-6">
          <Link href={`/register?ref=${code}`} className="block w-full py-3 maroon-gradient text-white rounded-full font-bold">🚀 Register with Referral →</Link>
          <div className="text-xs text-gray-400 mt-3">Redirecting in 2 sec...</div>
        </div>
      </div>
    </div>
  );
}
