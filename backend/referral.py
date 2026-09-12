"""
TSAP Matrimony — Referral + Bureau + Leaderboard
Pin-to-Pin Perfect Advanced — Startup Level
"""
import random
import string
from datetime import datetime
from typing import Dict, List

def generate_referral_code(tsap_id: str) -> str:
    """TSAP-M-2025-1042 → LAK42 short — 3 letters + 2 digits = 5 chars"""
    try:
        seq = tsap_id.split("-")[-1]
        # Short code: use seq last 2 digits + random
        return f"{random.choice(['LAK','RAJ','SAI','SRI','POO','KAR'])}{seq[-2:]}"
    except:
        return f"{random.choice(['LAK','RAJ','SAI'])}{random.randint(10,99)}"

def generate_short_code(name: str, existing_codes: list = []) -> str:
    """Short code — 3 letters + 2 digits = 5 chars — LAK42 — easy enter!"""
    clean = "".join(c for c in name if c.isalpha()).upper()
    base = clean[:3].ljust(3, "X")  # LAK, RAJ, SRI
    for _ in range(100):
        num = random.randint(10,99)
        code = f"{base}{num}"  # LAK42
        if code not in existing_codes:
            return code
    return f"{base}{random.randint(100,999)}"

def generate_broker_code(name: str) -> str:
    """Broker short — RAJ01 — 3 letters + 2 digits — 5 chars"""
    return generate_short_code(name)

def generate_bureau_code(name: str) -> str:
    """Bureau short — SRI1 / SAI01 — 3-4 letters + 1-2 digits — 4-5 chars — short, easy"""
    clean = "".join(c for c in name if c.isalpha()).upper()
    base = clean[:3]
    # Try 1 digit first for bureau — SRI1 (4 chars) — even shorter!
    for _ in range(10):
        code = f"{base}{random.randint(1,9)}"  # SRI1
        return code
    return generate_short_code(name)

def parse_referral_type(code: str) -> str:
    if not code: return "NONE"
    code = code.upper()
    if code.startswith("BROKER-"): return "BROKER"
    if code.startswith("BUREAU-"): return "BUREAU"
    if code.startswith("TSAP-REF-"): return "USER"
    # phone number referral
    if code.isdigit() and len(code)>=10: return "PHONE"
    return "USER"

def calculate_commission(referral_type: str, plan_amount: int) -> int:
    """Per pay commission — NEW: ₹50 for first ₹99 pay — 50% — viral — no thappu!"""
    if plan_amount==99:
        # All types — USER, LADY, STUDENT, INFLUENCER, BROKER — ₹50 first pay — viral!
        return 50
    if plan_amount==299:
        if referral_type=="BROKER": return 90
        if referral_type=="BUREAU": return 90
        return 50
    if plan_amount==999:
        if referral_type=="BROKER": return 200
        if referral_type=="BUREAU": return 300
        return 100
    return 0

def check_bonus_eligibility(referrer_stats: Dict) -> Dict:
    """25 pays/month → ₹500 bonus + 10 profiles share"""
    paid = referrer_stats.get("paid_count", 0)
    if paid>=50:
        return {"eligible": True, "bonus": 1200, "reward": "50 profiles share + Verified Badge + ₹1200", "tier": "GOLD"}
    if paid>=25:
        return {"eligible": True, "bonus": 500, "reward": "10 profiles share + ₹500", "tier": "SILVER"}
    return {"eligible": False, "bonus": 0, "reward": "", "tier": "BRONZE"}

def process_referral_payment(referred_user: Dict, referrer_code: str, plan_amount: int, all_users: List[Dict]) -> Dict:
    """
    referred_user pay chesaka — referrer ki commission + credits
    Pin-to-Pin:
    1. Referral code parse → type
    2. Commission calculate
    3. Referrer find (by code or phone)
    4. Commission add to referrer wallet + credits if USER
    5. Bonus check
    6. Leaderboard update
    """
    ref_type = parse_referral_type(referrer_code)
    commission = calculate_commission(ref_type, plan_amount)

    # Find referrer (mock — real DB lo search)
    referrer = None
    for u in all_users:
        if u.get("referral_code")==referrer_code or u.get("phone")==referrer_code or u.get("tsap_id")==referrer_code:
            referrer = u
            break

    if not referrer:
        return {"success": False, "message": f"Referrer {referrer_code} not found, commission pending — admin will verify"}

    # Add commission
    referrer["wallet"] = referrer.get("wallet", 0) + commission
    if ref_type=="USER":
        referrer["credits"] = referrer.get("credits", 0) + 2  # 2 free credits for user referral

    # Update stats
    referrer["referral_stats"] = referrer.get("referral_stats", {"total":0, "paid_count":0})
    referrer["referral_stats"]["paid_count"] += 1

    bonus = check_bonus_eligibility(referrer["referral_stats"])

    # Notification message Telugu
    msg = f"🎉 Congrats! Me friend {referred_user['tsap_id']} pay chesadu (₹{plan_amount}). Meeku ₹{commission} vachindi!"
    if ref_type=="USER":
        msg += f" + 2 free credits! Total credits: {referrer['credits']}"
    if bonus["eligible"]:
        msg += f" 🏆 Bonus! {bonus['reward']}"

    return {
        "success": True,
        "referrer_id": referrer.get("tsap_id"),
        "commission": commission,
        "bonus": bonus,
        "message_telugu": msg,
        "referrer_new_credits": referrer.get("credits",0),
        "referrer_wallet": referrer.get("wallet",0)
    }

def get_leaderboard(all_users: List[Dict], limit=10) -> List[Dict]:
    """Top referrers — weekly"""
    # sort by paid_count
    sorted_users = sorted(all_users, key=lambda x: x.get("referral_stats", {}).get("paid_count",0), reverse=True)
    board = []
    for u in sorted_users[:limit]:
        stats = u.get("referral_stats", {"total":0, "paid_count":0})
        board.append({
            "name": u.get("name", u.get("tsap_id","Unknown")),
            "code": u.get("referral_code",""),
            "refers": stats.get("total",0),
            "paid": stats.get("paid_count",0),
            "earned": u.get("wallet",0),
            "tier": check_bonus_eligibility(stats).get("tier","BRONZE")
        })
    return board

def generate_bureau_white_label_card(original_card_path: str, bureau_name: str, bureau_code: str, output_path: str) -> str:
    """Card meeda 'Via Sri Sai Bureau' add cheyadam"""
    # In real: Pillow tho original card meeda text overlay
    # Mock: return same path with note
    return output_path + f" [White-label: Via {bureau_name} | {bureau_code}]"
