/**
 * 🛡️ WAVE 9 — apiFetch: single place for API calls
 *  • auth token (X-Tsap-Token) — private endpoints IDOR fix
 *  • admin key (X-Admin-Key) — PII endpoints
 *  • timeout + retry + safe JSON parse + Telugu error normalisation
 */

export const TOKEN_KEY = "tsap_token";
export const TSAP_KEY = "tsap_id";
export const ADMIN_KEY_STORE = "tsap_admin_key";

export type ApiResult<T> = {
  ok: boolean;
  status: number;
  data: T | null;
  error: string;
  errorTelugu: string;
  needsLogin: boolean;
  needsAdminKey: boolean;
  retryAfter?: number;
};

export function getToken(): string {
  if (typeof window === "undefined") return "";
  try { return localStorage.getItem(TOKEN_KEY) || ""; } catch { return ""; }
}

export function setToken(token: string, tsapId?: string) {
  if (typeof window === "undefined") return;
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    if (tsapId) localStorage.setItem(TSAP_KEY, tsapId);
  } catch { /* private mode */ }
}

export function getAdminKey(): string {
  if (typeof window === "undefined") return "";
  try { return localStorage.getItem(ADMIN_KEY_STORE) || ""; } catch { return ""; }
}

export function setAdminKey(key: string) {
  if (typeof window === "undefined") return;
  try { localStorage.setItem(ADMIN_KEY_STORE, key); } catch { /* ignore */ }
}

export function clearAuth() {
  if (typeof window === "undefined") return;
  try { localStorage.removeItem(TOKEN_KEY); } catch { /* ignore */ }
}

type Opts = {
  method?: "GET" | "POST" | "DELETE" | "PUT";
  body?: unknown;
  form?: FormData;
  admin?: boolean;
  timeoutMs?: number;
  retries?: number;
  cache?: RequestCache;
};

export async function apiFetch<T = unknown>(path: string, opts: Opts = {}): Promise<ApiResult<T>> {
  const { method = "GET", body, form, admin = false, timeoutMs = 12000, retries = 1, cache } = opts;
  const headers: Record<string, string> = {};
  const token = getToken();
  if (token) headers["X-Tsap-Token"] = token;
  if (admin) {
    const key = getAdminKey();
    if (key) headers["X-Admin-Key"] = key;
  }
  if (body !== undefined) headers["Content-Type"] = "application/json";

  for (let attempt = 0; attempt <= retries; attempt++) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const res = await fetch(path, {
        method,
        headers,
        body: form ? form : body !== undefined ? JSON.stringify(body) : undefined,
        signal: ctrl.signal,
        cache,
      });
      clearTimeout(timer);
      const text = await res.text();
      let data: T | null = null;
      try { data = text ? (JSON.parse(text) as T) : null; } catch { data = null; }
      const d = (data || {}) as Record<string, unknown>;
      const telugu = String(d.message_telugu || d.detail || d.error || "");
      const isJson = data !== null && typeof data === "object";
      if (res.ok) {
        return { ok: true, status: res.status, data, error: "", errorTelugu: telugu, needsLogin: false, needsAdminKey: false };
      }
      // 5xx → retry once (server hiccup)
      if (res.status >= 500 && attempt < retries) { await new Promise((r) => setTimeout(r, 400)); continue; }
      return {
        ok: false,
        status: res.status,
        data: isJson ? data : null,
        error: String(d.error || d.detail || res.statusText || "request_failed"),
        errorTelugu: telugu || (res.status === 401
          ? "🔒 Mee account ki OTP login cheyyandi"
          : res.status === 403
          ? "🔒 Ee data ki access ledu (admin key / owner matrame)"
          : res.status === 429
          ? "⏳ Chala fast ga try chestunnaru — konchem aagi malli try cheyyandi"
          : "⚠️ Server problem — malli try cheyyandi"),
        needsLogin: res.status === 401,
        needsAdminKey: res.status === 403 && admin,
        retryAfter: Number(res.headers.get("Retry-After") || d.retry_after || 0) || undefined,
      };
    } catch (err) {
      clearTimeout(timer);
      if (attempt < retries) { await new Promise((r) => setTimeout(r, 400)); continue; }
      const aborted = (err as Error)?.name === "AbortError";
      return {
        ok: false, status: 0, data: null,
        error: aborted ? "timeout" : "network_error",
        errorTelugu: aborted ? "⏱️ Server slow ga undi — malli try cheyyandi" : "📡 Internet/server connection ledu — check cheyyandi",
        needsLogin: false, needsAdminKey: false,
      };
    }
  }
  return { ok: false, status: 0, data: null, error: "unreachable", errorTelugu: "⚠️ Try cheyyandi", needsLogin: false, needsAdminKey: false };
}

/** GET shorthand */
export const apiGet = <T = unknown>(path: string, admin = false) => apiFetch<T>(path, { admin });

/** POST shorthand */
export const apiPost = <T = unknown>(path: string, body?: unknown, admin = false) =>
  apiFetch<T>(path, { method: "POST", body: body ?? {}, admin });

/** Local (offline) safe JSON read */
export function readLocal<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch { return fallback; }
}

export function writeLocal(key: string, value: unknown) {
  if (typeof window === "undefined") return;
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* ignore */ }
}

/** fetch() ki auth headers (token + admin key) — muttadi calls ki convenience */
export function authHeaders(admin = false): Record<string, string> {
  const h: Record<string, string> = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) h["X-Tsap-Token"] = token;
  if (admin) {
    const key = getAdminKey();
    if (key) h["X-Admin-Key"] = key;
  }
  return h;
}
