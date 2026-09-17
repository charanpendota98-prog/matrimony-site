"""
📝 WAVE 15 — CMS (Admin-curated content: custom pages + success stories + banners)
====================================================================================
Admin website ni customize cheyyochu — code marchakunda:
  • PAGES   — custom pages (slug: /p/about-us) — EN+TE title/body, photos, tags
  • STORIES — featured success stories (couple photo + story + tags + district)
  • BANNERS — announcement strips (homepage/pricing/all pages, link, order)
Public read (published only) · Admin CRUD · tags filter · 1-click seed.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_FILE = os.path.join(BASE_DIR, "cms15.json")

PAGES: List[Dict] = []
STORIES: List[Dict] = []
BANNERS: List[Dict] = []
_SEQ = {"ST": 0, "BN": 0}

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9\-]{1,58}[a-z0-9]$")


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")


def _persist() -> None:
    try:
        with open(PERSIST_FILE, "w", encoding="utf-8") as f:
            json.dump({"pages": PAGES[-200:], "stories": STORIES[-300:], "banners": BANNERS[-100:]},
                      f, ensure_ascii=False)
    except Exception:
        pass


def _restore() -> None:
    try:
        if os.path.exists(PERSIST_FILE):
            d = json.load(open(PERSIST_FILE, encoding="utf-8")) or {}
            PAGES.extend(d.get("pages", []))
            STORIES.extend(d.get("stories", []))
            BANNERS.extend(d.get("banners", []))
            for s in STORIES:
                try:
                    _SEQ["ST"] = max(_SEQ["ST"], int(str(s.get("id", "ST-0")).split("-")[-1]))
                except Exception:
                    pass
            for b in BANNERS:
                try:
                    _SEQ["BN"] = max(_SEQ["BN"], int(str(b.get("id", "BN-0")).split("-")[-1]))
                except Exception:
                    pass
    except Exception:
        pass


_restore()


def _tags(raw) -> List[str]:
    if isinstance(raw, str):
        raw = [x.strip() for x in raw.split(",")]
    out = []
    for t in (raw or []):
        t = str(t or "").strip().lower()[:30]
        if t and t not in out:
            out.append(t)
    return out[:10]


def _photos(raw) -> List[str]:
    if isinstance(raw, str):
        raw = [raw]
    out = []
    for u in (raw or []):
        u = str(u or "").strip()[:500]
        if u and (u.startswith("/") or u.startswith("http")) and u not in out:
            out.append(u)
    return out[:8]


# ------------------------------------------------------------------ PAGES
def upsert_page(slug: str, title_en: str, title_te: str, body_en: str = "", body_te: str = "",
                photos=None, tags=None, published: bool = True, order: int = 0) -> Dict:
    slug = str(slug or "").strip().lower()
    if not _SLUG_RE.match(slug):
        return {"success": False, "message_telugu": "⚠️ slug: a–z, 0–9, hyphen (ex: about-us)"}
    if not str(title_en or "").strip():
        return {"success": False, "message_telugu": "⚠️ English title kavali"}
    p = next((x for x in PAGES if x.get("slug") == slug), None)
    data = {"slug": slug, "title_en": str(title_en).strip()[:200], "title_te": str(title_te or "").strip()[:200],
            "body_en": str(body_en or "")[:20000], "body_te": str(body_te or "")[:20000],
            "photos": _photos(photos), "tags": _tags(tags), "published": bool(published),
            "order": int(order or 0), "updated_at": _now()}
    if p:
        p.update(data)
        msg = f"✅ Page /p/{slug} update ayyindi"
    else:
        data["created_at"] = _now()
        PAGES.append(data)
        msg = f"✅ Page /p/{slug} ready!"
    _persist()
    return {"success": True, "page": next(x for x in PAGES if x.get("slug") == slug), "message_telugu": msg}


def get_page(slug: str) -> Optional[Dict]:
    return next((x for x in PAGES if x.get("slug") == str(slug or "").strip().lower()), None)


def list_pages(published_only: bool = True) -> List[Dict]:
    out = [p for p in PAGES if not published_only or p.get("published")]
    return sorted(out, key=lambda x: (x.get("order", 0), x.get("slug", "")))


# ------------------------------------------------------------------ STORIES
def upsert_story(sid: str = "", groom: str = "", bride: str = "", photo: str = "",
                 story_en: str = "", story_te: str = "", district: str = "",
                 wedding_date: str = "", tags=None, published: bool = True) -> Dict:
    global _SEQ
    if not str(groom or "").strip() or not str(bride or "").strip():
        return {"success": False, "message_telugu": "⚠️ Groom + bride names kavali"}
    if sid:
        s = next((x for x in STORIES if x.get("id") == sid), None)
        if not s:
            return {"success": False, "message_telugu": "⚠️ Story dorakaledu"}
    else:
        _SEQ["ST"] += 1
        s = {"id": f"ST-{_SEQ['ST']:04d}", "created_at": _now()}
        STORIES.append(s)
        sid = s["id"]
    s.update({"groom": str(groom).strip()[:80], "bride": str(bride).strip()[:80],
              "photo": _photos([photo])[0] if photo else s.get("photo", ""),
              "story_en": str(story_en or "")[:5000], "story_te": str(story_te or "")[:5000],
              "district": str(district or "").strip()[:40], "wedding_date": str(wedding_date or "")[:10],
              "tags": _tags(tags) or s.get("tags", []), "published": bool(published),
              "updated_at": _now()})
    _persist()
    return {"success": True, "story": s, "message_telugu": f"✅ Success story {sid} ready! 💑"}


def list_stories(tag: str = "", published_only: bool = True, limit: int = 20) -> List[Dict]:
    out = [x for x in STORIES if (not published_only or x.get("published"))
           and (not tag or tag.lower() in (x.get("tags") or []))]
    out.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return out[:max(1, min(int(limit or 20), 100))]


# ------------------------------------------------------------------ BANNERS
def upsert_banner(bid: str = "", text_en: str = "", text_te: str = "", link: str = "",
                  pages=None, active: bool = True, order: int = 0) -> Dict:
    global _SEQ
    if not str(text_en or "").strip():
        return {"success": False, "message_telugu": "⚠️ Banner text (English) kavali"}
    if bid:
        b = next((x for x in BANNERS if x.get("id") == bid), None)
        if not b:
            return {"success": False, "message_telugu": "⚠️ Banner dorakaledu"}
    else:
        _SEQ["BN"] += 1
        b = {"id": f"BN-{_SEQ['BN']:04d}", "created_at": _now()}
        BANNERS.append(b)
        bid = b["id"]
    pg = pages if isinstance(pages, list) else [str(pages or "all")]
    pg = [str(x).strip().lower()[:20] or "all" for x in pg][:10] or ["all"]
    b.update({"text_en": str(text_en).strip()[:300], "text_te": str(text_te or "").strip()[:300],
              "link": str(link or "").strip()[:300], "pages": pg, "active": bool(active),
              "order": int(order or 0), "updated_at": _now()})
    _persist()
    return {"success": True, "banner": b, "message_telugu": f"✅ Banner {bid} ready!"}


def list_banners(page: str = "", admin: bool = False) -> List[Dict]:
    pg = str(page or "").strip().lower()
    out = [x for x in BANNERS if (admin or x.get("active"))
           and (not pg or "all" in (x.get("pages") or []) or pg in (x.get("pages") or []))]
    return sorted(out, key=lambda x: (x.get("order", 0), x.get("id", "")))


# ------------------------------------------------------------------ DELETE/TAGS/SEED
def delete_item(kind: str, iid: str) -> Dict:
    store = {"page": PAGES, "story": STORIES, "banner": BANNERS}.get(str(kind or "").lower())
    if store is None:
        return {"success": False, "message_telugu": "⚠️ kind: page/story/banner"}
    key = "slug" if str(kind).lower() == "page" else "id"
    before = len(store)
    store[:] = [x for x in store if str(x.get(key, "")) != str(iid or "")]
    if len(store) == before:
        return {"success": False, "message_telugu": "⚠️ Item dorakaledu"}
    _persist()
    return {"success": True, "message_telugu": f"✅ {iid} delete ayyindi"}


def all_tags() -> List[str]:
    out: List[str] = []
    for x in PAGES + STORIES:
        for t in (x.get("tags") or []):
            if t not in out:
                out.append(t)
    return sorted(out)


def seed_cms() -> Dict:
    """Admin 1-click: demo pages + stories (edit/delete cheyochu)."""
    added = []
    if not get_page("about-us"):
        upsert_page("about-us", "About Mana Vivaha", "మన వివాహ గురించి",
                    "TS & AP's most advanced Telugu matrimony — region, religion, caste and special channels with smart auto-posting.",
                    "TS & AP ల అత్యంత అధునాతన తెలుగు మ్యాట్రిమోనీ — region, religion, caste, special ఛానళ్లతో స్మార్ట్ ఆటో-పోస్టింగ్.",
                    tags=["info", "trust"])
        added.append("page:about-us")
    if not get_page("contact-us"):
        upsert_page("contact-us", "Contact Us", "మమ్మల్ని సంప్రదించండి",
                    "WhatsApp/Telegram support + email care@manavivaha.in. 10am–8pm IST, all days.",
                    "వాట్సాప్/టెలిగ్రామ్ support + email care@manavivaha.in. ఉదయం 10 – రాత్రి 8, అన్ని రోజులు.",
                    tags=["info", "support"])
        added.append("page:contact-us")
    if not STORIES:
        upsert_story("", "Ravi Kumar", "Lakshmi", "", "Met through Mana Vivaha TS channel — married in 3 months!",
                     "మన వివాహ TS ఛానల్ ద్వారా పరిచయం — 3 నెలల్లో పెళ్లి!", "Hyderabad", "2026-02-14",
                     tags=["hyderabad", "love"])
        upsert_story("", "Suresh", "Anitha", "", "Parents found the perfect alliance via caste channel.",
                     "కుల ఛానల్ ద్వారా తల్లిదండ్రులు మంచి సంబంధం కుదిర్చారు.", "Vijayawada", "2026-05-20",
                     tags=["vijayawada", "arranged"])
        added += ["story×2"]
    return {"success": True, "added": added,
            "message_telugu": f"✅ CMS seed: {', '.join(added) or 'already unnai'}"}


def cms_stats() -> Dict:
    return {"pages": len(PAGES), "pages_live": sum(1 for p in PAGES if p.get("published")),
            "stories": len(STORIES), "stories_live": sum(1 for s in STORIES if s.get("published")),
            "banners": len(BANNERS), "banners_live": sum(1 for b in BANNERS if b.get("active")),
            "tags": len(all_tags())}
