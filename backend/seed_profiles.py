"""
Generate 40 seed profiles (20 brides, 20 grooms) for TSBRIDE, TSGROOM1
Simple MVP — no deep verification
"""
import json, random, os
from datetime import datetime

# TS districts
districts = ["Hyderabad","Nalgonda","Warangal","Karimnagar","Khammam","Nizamabad","Medak","Rangareddy","Mahabubnagar","Adilabad"]
castes = ["Reddy","Kamma","Kapu","Velama","Vysya","Brahmin","Goud","Yadav","Mudiraj","Padmashali"]
educations = ["BTech","MTech","Degree","MBA","MBBS","Inter","10th"]
jobs = ["Software","Govt Job","Private Job","Business","Doctor","Engineer","Teacher"]
mandals = ["Gachibowli","Kukatpally","Madhapur","LB Nagar","Uppal","Secunderabad","Ameerpet","Dilsukhnagar"]

def gen_profile(gender, idx):
    age = random.randint(22,28) if gender=="Bride" else random.randint(25,32)
    height = random.choice(["5'2\"","5'4\"","5'5\"","5'6\""]) if gender=="Bride" else random.choice(["5'6\"","5'8\"","5'10\"","6'0\""])
    caste = random.choice(castes)
    district = random.choice(districts)
    edu = random.choice(educations)
    job = random.choice(jobs)
    salary = random.choice(["40k","60k","80k","1L","1.2L"])
    gothram = random.choice(["Bharadwaj","Koundinya","Kashyapa","Vashista"])
    star = random.choice(["Rohini","Mrigasira","Arudra","Punarvasu"])
    tsap_id = f"TSAP-{'F' if gender=='Bride' else 'M'}-2025-{1000+idx}"
    return {
        "tsap_id": tsap_id,
        "gender": gender,
        "age": age,
        "height": height,
        "caste": caste,
        "sub_caste": "",
        "gothram": gothram,
        "star": star,
        "education": edu,
        "job": job,
        "salary": salary,
        "state": "TS",
        "district": district,
        "mandal": random.choice(mandals),
        "marital_status": "Pelli Kaledu",
        "phone": f"98480{random.randint(10000,99999)}",
        "referral_code": f"TSAP-REF-{1000+idx}",
        "referred_by": "",
        "photo_urls": [f"/photos/{tsap_id}_1.jpg"],
        "card_url": f"/cards/{tsap_id}.png",
        "is_verified": True,
        "is_approved": True,
        "privacy_mode": "public",
        "credits": 3,
        "plan": "FREE",
        "created_at": datetime.utcnow().isoformat(),
        "score": random.randint(75,95),
        "reasons": [f"Same caste {caste}", f"Same district {district}", f"Age gap perfect"],
        "expectations": f"Same caste, {district} near, {job}"
    }

profiles = []
for i in range(20):
    profiles.append(gen_profile("Bride", i+1))
for i in range(20):
    profiles.append(gen_profile("Groom", 21+i))

# Save
os.makedirs("../frontend/public/seed", exist_ok=True)
with open("../frontend/public/seed/seed_profiles.json","w") as f:
    json.dump(profiles, f, indent=2)

# Also save for backend
with open("seed_profiles.json","w") as f:
    json.dump(profiles, f, indent=2)

print(f"Generated {len(profiles)} profiles")
print(f"Brides: {len([p for p in profiles if p['gender']=='Bride'])} -> @TSBRIDE")
print(f"Grooms: {len([p for p in profiles if p['gender']=='Groom'])} -> @TSGROOM1")
for p in profiles[:3]:
    print(p["tsap_id"], p["gender"], p["age"], p["caste"], p["district"], p["job"])
