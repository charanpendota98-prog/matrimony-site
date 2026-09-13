"""
TSAP Matrimony — Credits System
Pin-to-Pin Perfect Advanced
FREE 3, ₹99=10, ₹299=50, etc. Limit ayyaka malli pay.
"""
from datetime import datetime, timedelta
from typing import Dict

PLANS = {
    "FREE": {"price": 0, "credits": 3, "daily": 0, "validity_days": 365, "name_telugu": "Free — 3 profiles (lock)"},
    "TRIAL_99": {"price": 99, "credits": 10, "daily": 2, "validity_days": 30, "name_telugu": "Trial — 10 numbers + daily 2"},
    "PREMIUM_299": {"price": 299, "credits": 50, "daily": 5, "validity_days": 60, "name_telugu": "Premium — 50 numbers + daily 5"},
    "VIP_999": {"price": 999, "credits": 9999, "daily": 10, "validity_days": 90, "name_telugu": "VIP Unlimited"},
    "BUREAU_999": {"price": 999, "credits": 25, "daily": 5, "validity_days": 30, "name_telugu": "Bureau Starter"},
    "BUREAU_2999": {"price": 2999, "credits": 9999, "daily": 10, "validity_days": 30, "name_telugu": "Bureau Pro"},
}

def get_plan_details(plan_key: str) -> Dict:
    return PLANS.get(plan_key, PLANS["FREE"])

def can_view_number(user_credits: int) -> bool:
    return user_credits > 0

def deduct_credit(user: Dict) -> Dict:
    """1 credit = 1 number view"""
    if user["credits"] <= 0:
        return {"success": False, "message_telugu": "⚠️ Me credits ayipoyayi! Malli ₹99 tho 10 credits pondandi", "credits": 0}
    user["credits"] -= 1
    # log transaction
    return {"success": True, "credits": user["credits"], "message_telugu": f"✅ Number unlock ayyindi! Migilina credits: {user['credits']}"}

def add_credits(user: Dict, plan_key: str, payment_verified: bool = True) -> Dict:
    if not payment_verified:
        return {"success": False, "message": "Payment not verified"}
    plan = get_plan_details(plan_key)
    user["credits"] += plan["credits"]
    user["plan"] = plan_key
    user["plan_expiry"] = datetime.utcnow() + timedelta(days=plan["validity_days"])
    return {"success": True, "credits": user["credits"], "plan": plan_key, "expiry": user["plan_expiry"], "message_telugu": f"🎉 {plan['credits']} credits add ayyayi! Plan: {plan['name_telugu']}"}

def add_referral_bonus(user: Dict, bonus_credits: int = 2) -> Dict:
    user["credits"] += bonus_credits
    return {"success": True, "credits": user["credits"], "message_telugu": f"🎉 Referral bonus! Meeku {bonus_credits} free credits vachayi"}

def add_admin_gift(user: Dict, gift_credits: int = 10) -> Dict:
    user["credits"] += gift_credits
    user["plan"] = "PREMIUM_299"  # gift as premium
    return {"success": True, "credits": user["credits"], "message_telugu": f"💎 Admin gift! Meeku {gift_credits} credits FREE + Premium! — TSAP Team"}

def is_plan_expired(user: Dict) -> bool:
    if not user.get("plan_expiry"): return False
    return datetime.utcnow() > user["plan_expiry"]

def get_daily_quota(plan_key: str) -> int:
    return get_plan_details(plan_key).get("daily", 0)

# ID Search — always allowed even if credits 0, but number needs credit
def can_search_id(user: Dict, search_id: str) -> Dict:
    """ID search eppudu open — profile chudochu, number ki credit kavali"""
    return {
        "can_view_profile": True,
        "can_view_number": can_view_number(user["credits"]),
        "is_photo_blur": user["plan"]=="FREE" and not user.get("is_paid", False),  # free ki blur
        "message": "ID search always open — profile chudochu, number ki credit kavali" if not can_view_number(user["credits"]) else "Full access"
    }
