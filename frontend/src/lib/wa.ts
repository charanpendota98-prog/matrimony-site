/**
 * WhatsApp channel links — ఒక్క చోటే configure చెయ్యండి.
 * =====================================================
 * WhatsApp channel create చేసి invite link ఇక్కడ key తో పెడితే —
 * ఆ channel కి సంబంధించిన అన్ని చోట్లా (caste pages, /castes cards,
 * register success, /channels) ఆటోమేటిక్‌గా WhatsApp button వస్తుంది.
 *
 * Key = lib/channels.ts లోని channel "key" (lowercase).
 * ఉదా: c_reddy_bride, c_kamma_groom, official, ts_bride…
 *
 * Backend (docker .env) లో కూడా ఇలా పెట్టవచ్చు (server-side posting కోసం):
 *   WA_CHANNEL_LINKS={"c_reddy_bride":"https://whatsapp.com/channel/xxx"}
 */
export const WA_CHANNEL_LINKS: Record<string, string> = {
  // "official": "https://whatsapp.com/channel/XXXX",
  // "c_reddy_bride": "https://whatsapp.com/channel/XXXX",
  // "c_reddy_groom": "https://whatsapp.com/channel/XXXX",
};

/** channel key → WhatsApp link (leda empty string) */
export function waLink(channelKey?: string): string {
  if (!channelKey) return "";
  return WA_CHANNEL_LINKS[channelKey] || "";
}
