"""
TSAP Matrimony — Matching Engine 0-100 + Personalized Reason Generator
Pin-to-Pin Perfect Advanced — Never Before
"""
from typing import List, Dict
import random

# Weightage
WEIGHTS = {
    "age": 25,
    "caste": 20,
    "location": 15,
    "education": 15,
    "job_salary": 10,
    "height": 5,
    "horoscope": 5,
    "marital": 5,
}

EDU_LEVELS = {
    "10th": 1, "Inter": 2, "Degree": 3, "BTech": 4, "MTech": 5, "MBA": 4, "MBBS": 6, "PhD": 7, "Others": 2
}

def calculate_age_score(user_age: int, match_age: int, user_gender: str) -> int:
    """Abbayi 1-5 years pedda = full, thakkuva theda = thakkuva"""
    if user_gender == "Groom":  # abbayi kosam ammai
        diff = user_age - match_age
        if 1 <= diff <= 5: return WEIGHTS["age"]
        elif diff == 0: return 20
        elif diff < 0: return 5  # ammai pedda
        else: return max(0, 25 - (diff-5)*3)
    else:  # ammai kosam abbayi
        diff = match_age - user_age
        if 1 <= diff <= 5: return WEIGHTS["age"]
        elif diff == 0: return 20
        elif diff < 0: return 5
        else: return max(0, 25 - (diff-5)*3)

def calculate_caste_score(user_caste: str, match_caste: str, user_wants_same: bool) -> int:
    if user_wants_same:
        return WEIGHTS["caste"] if user_caste==match_caste else 0
    else:
        # intercaste ok — same ki 20, vere ki 10
        return WEIGHTS["caste"] if user_caste==match_caste else 10

def calculate_location_score(user_district: str, match_district: str, user_state: str, match_state: str, user_mandal: str, match_mandal: str) -> int:
    if user_district==match_district and user_mandal and match_mandal and user_mandal.lower()==match_mandal.lower():
        return 15  # same mandal — super
    if user_district==match_district:
        return 15
    if user_state==match_state:
        return 10
    return 5

def calculate_education_score(user_edu: str, match_edu: str) -> int:
    u = EDU_LEVELS.get(user_edu, 2)
    m = EDU_LEVELS.get(match_edu, 2)
    diff = abs(u-m)
    if diff==0: return 15
    if diff==1: return 12
    if diff==2: return 8
    return 4

def calculate_job_score(user_job: str, match_job: str) -> int:
    if user_job==match_job: return 10
    # Govt + Govt = full, Software+Software = full
    if "Govt" in user_job and "Govt" in match_job: return 10
    if "Software" in user_job and "Software" in match_job: return 10
    return 6

def calculate_height_score(user_height: str, match_height: str, user_gender: str) -> int:
    # Simple: abbayi podavuga unte full
    try:
        def to_inches(h: str):
            # "5'8"" -> 68
            parts = h.replace('"','').split("'")
            return int(parts[0])*12 + int(parts[1] or 0)
        uh = to_inches(user_height)
        mh = to_inches(match_height)
        if user_gender=="Groom":
            return 5 if uh>=mh else 2
        else:
            return 5 if mh>=uh else 2
    except:
        return 3

def calculate_horoscope_score(user_star: str, match_star: str) -> int:
    if not user_star or not match_star: return 3
    if user_star==match_star: return 5
    return 3  # Phase-2: real panchangam logic

def calculate_marital_score(user_marital: str, match_marital: str) -> int:
    return 5 if user_marital==match_marital else 2

def calculate_match_score(user: Dict, match: Dict, user_wants_same_caste: bool=True) -> int:
    age = calculate_age_score(user["age"], match["age"], user["gender"])
    caste = calculate_caste_score(user["caste"], match["caste"], user_wants_same_caste)
    loc = calculate_location_score(user["district"], match["district"], user["state"], match["state"], user.get("mandal",""), match.get("mandal",""))
    edu = calculate_education_score(user["education"], match["education"])
    job = calculate_job_score(user["job"], match["job"])
    height = calculate_height_score(user["height"], match["height"], user["gender"])
    horo = calculate_horoscope_score(user.get("star",""), match.get("star",""))
    marital = calculate_marital_score(user["marital_status"], match["marital_status"])
    total = age+caste+loc+edu+job+height+horo+marital
    return min(100, total)

def generate_personalized_reasons(user: Dict, match: Dict, score: int) -> List[str]:
    """Nuvvu ilaga anukunnavu, idi ilaga set avuthadu — Telugu lo"""
    reasons = []
    # Location
    if user["district"]==match["district"]:
        if user.get("mandal") and match.get("mandal") and user["mandal"].lower()==match["mandal"].lower():
            reasons.append(f"Nuvvu {user['mandal']} kavali annavu → {match['gender']} kooda {match['mandal']} lone — super near!")
        else:
            reasons.append(f"Nuvvu {user['district']} kavali annavu → {match['gender']} kooda {match['district']} lone")
    elif user["state"]==match["state"]:
        reasons.append(f"Nuvvu {user['state']} kavali annavu → {match['gender']} kooda {user['state']} lone")

    # Job
    if user["job"]==match["job"]:
        reasons.append(f"Nuvvu {user['job']} kavali annavu → {match['gender']} kooda {match['job']} ({match.get('salary','')})")
    elif "Govt" in user["job"] and "Govt" in match["job"]:
        reasons.append(f"Govt job — iddaru Govt, secure future!")

    # Caste
    if user["caste"]==match["caste"]:
        reasons.append(f"Nuvvu {user['caste']} kavali annavu → {match['gender']} kooda {user['caste']}, gothram kooda {user.get('gothram','')} != {match.get('gothram','')} (safe)")

    # Age
    diff = abs(user["age"]-match["age"])
    if 1 <= diff <= 5:
        reasons.append(f"Age gap {diff} years — perfect, understanding baguntundi")

    # Education
    if user["education"]==match["education"]:
        reasons.append(f"Education iddaru {user['education']} — matching thoughts")

    # Mandal proximity
    if not reasons:
        reasons.append(f"Location + Education + Caste 3 kalisi {score}% set avuthundi")

    # Limit to 3 best
    return reasons[:3]

def find_top_matches(user: Dict, all_profiles: List[Dict], limit=10, min_score=70, wants_same_caste=True) -> List[Dict]:
    """Opposite gender only, 70%+ only, sorted by score"""
    opposite = "Bride" if user["gender"]=="Groom" else "Groom"
    scored = []
    for p in all_profiles:
        if p["gender"]!=opposite: continue
        if p["tsap_id"]==user["tsap_id"]: continue
        score = calculate_match_score(user, p, wants_same_caste)
        if score < min_score: continue
        reasons = generate_personalized_reasons(user, p, score)
        scored.append({**p, "score": score, "reasons": reasons})

    # Sort by score desc, then verified, then recent
    scored.sort(key=lambda x: (x["score"], x.get("is_verified", False), x.get("created_at", "")), reverse=True)
    return scored[:limit]

# Mock test
if __name__=="__main__":
    user = {"tsap_id":"TSAP-M-1042","gender":"Groom","age":27,"height":"5'8\"","caste":"Reddy","district":"Nalgonda","state":"TS","mandal":"Gachibowli","education":"BTech","job":"Software","marital_status":"Pelli Kaledu","star":"Rohini","gothram":"Bharadwaj"}
    matches = [
        {"tsap_id":"TSAP-F-1042","gender":"Bride","age":24,"height":"5'4\"","caste":"Reddy","district":"Nalgonda","state":"TS","mandal":"Gachibowli","education":"BTech","job":"Software","marital_status":"Pelli Kaledu","star":"Rohini","gothram":"Koundinya","salary":"60k"},
        {"tsap_id":"TSAP-F-1043","gender":"Bride","age":23,"height":"5'2\"","caste":"Kamma","district":"Hyderabad","state":"TS","mandal":"","education":"MBA","job":"Private","marital_status":"Pelli Kaledu","star":"","gothram":"","salary":"40k"},
    ]
    top = find_top_matches(user, matches, limit=3)
    for t in top:
        print(t["tsap_id"], t["score"], t["reasons"])
