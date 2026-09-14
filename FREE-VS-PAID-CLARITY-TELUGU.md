# 🆓 FREE vs PAID — "3 profiles ఇస్తాం, కానీ numbers ఇవ్వము"

> **ఒక్క లైన్లో:** Register **100% FREE** → **3 profiles** చూడొచ్చు + **3 interests** పంపొచ్చు. కానీ
> **🔒 phone numbers ఇవ్వము** — interest పంపి వాళ్లు **accept** చేస్తే మాత్రమే రెండు వైపులా numbers
> exchange (WhatsApp లో). తరువాత మీ ఇష్టం — ₹99 → 5 profiles + boost.
>
> Website: **manavivaha.in/register** · Clarity API: **/api/free-plan** · Pricing: **manavivaha.in/pricing**

---

## 1. FREE లో ఏమి వస్తుంది (₹0)

| ✅ ఇచ్చేది | 🔒 ఇవ్వనిది |
|---|---|
| **3 profiles** full details (caste, education, job, family, porutham, match %) | **Phone numbers — ఇవ్వము** (98••••••45 అని మాత్రమే కనిపిస్తుంది) |
| **3 interests** పంపొచ్చు (వాళ్లకి మా WhatsApp నుండి మీ profile + card వెళ్తుంది) | Photo (privacy mode ఉన్న profiles కి blur) |
| Mee profile card FREE (Telugu, neat) + 52 channels లో auto-post | Chatting (లేదు — మనం chat platform కాదు) |
| Accept అయితే **numbers exchange** (consent తో) | 3 తరువాత: ₹99 → 5 profiles |
| Decline అయితే **credit refund** (loss లేదు) | — |

---

## 2. Numbers ఎప్పుడు వస్తాయి? (3 మార్గాలు)

1. **Interest → Accept** (ఉచితం): మీరు interest పంపండి → వాళ్లకి WhatsApp లో మీ profile వెళ్తుంది →
   వాళ్లు **accept** చేస్తే — రెండు వైపులా numbers WhatsApp లో (consent ఆధారంగా).
2. **Paid plan**: ₹99 → 5 requests, ₹199 → 12, ₹299 → 25, ₹499 → 50 — ఎక్కువ profiles చూసి, ఎక్కువ
   interests పంపొచ్చు (numbers అప్పుడు కూడా interest-accept తోనే).
3. **Admin/team assist**: ఏదైనా సందేహం ఉంటే మా support WhatsApp — మేము మధ్యలో ఉండి connect చేస్తాం.

> ⚠️ **number ఎప్పుడూ public గా కనిపించదు** — browser లో "view source" చేసినా రాదు (server నుండే lock చేస్తాం).

---

## 3. ఎందుకు ఇలా? (కారణాలు)

- 📵 **Spam/broker calls ఆపడానికి** — number public అయితే రోజుకి 20 calls.
- 🛡️ **రెండు వైపుల ఇష్టం** ఉన్నప్పుడే contact — అందరికీ safety.
- 💍 **Matrimony model** ఇదే: profile చూడటం free, contact మాత్రం consent/paid.
- 🔐 Mee number DB లో **encrypted** (`phone_encrypted`) గా store అవుతుంది(మా admin audit కి మాత్రమే).

---

## 4. Developer / audit (numbers leak కాకుండా)

| విషయం | వివరం |
|---|---|
| Lock helper | `interest.py` → `mask_phone()` (98••••••45) + `safe_user()` (contact fields లేవు + `contact_locked: true`) |
| Public API | `/api/search/{id}` · `/api/matches/{id}` · `/api/search` · `/api/views` · `/api/saved` · `/api/porutham` → **anni safe_user** (mundu search/matches full `phone` return చేసేవి — **fix అయ్యింది**) |
| Contact exchange | `/api/interest/respond` accept → `result.contact` + `owner_phone`/`requester_phone` (consent ఆధారంగా మాత్రమే) |
| Inbox/sent lock | accept కాకముందు `"🔒 accept cheyyandi"` / `"🔒 accept ayyaka"` (number కనిపించదు) |
| Clarity API | `GET /api/free-plan` — free vs paid, numbers rule, FAQ (Telugu) |
| Tests | `backend/test_privacy_contacts.py` — **53 checks** (endpoint-by-endpoint leak scan: 10-digit phone / phone_encrypted / email regex) |
| Frontend | `/register` clarity box (FREE enti / ఇవ్వనిది) · success screen "enti vachindi" card · `/matches` 🔒 chip + banner · `/pricing` FREE vs PAID boxes |

---

## 5. WhatsApp కి పంపాల్సిన reply (copy-paste)

```
🆓 Mana Vivaha — FREE vs PAID (clear ga)

FREE (₹0 — card details అవసరం లేదు):
✅ 3 profiles full details chudochu (caste, education, job, family, porutham)
✅ 3 interests pampochu — vaallaki mana WhatsApp nunchi mee profile + card veltundi
✅ Mee profile card free + 52 channels lo auto-post
🔒 KANI phone numbers ivvamu (98••••••45 ani matrame kanipisthundi)
🔒 Photo (privacy profiles ki blur) · Chatting ledu

Numbers eppudu vastayi?
1) Interest pampandi → vaallu ACCEPT cheste → rendu vaipula numbers WhatsApp lo (consent tho)
2) Ekkuva profiles kavali ante: ₹99 → 5 · ₹199 → 12 · ₹299 → 25 · ₹499 → 50
   (number kooda accept tho ne — public ga eppudu kanipinchadu)

Enduku ila? Spam/broker calls aapadaniki + rendu vaipula istam unte matrame contact.
Mee number DB lo encrypted ga untundi. Decline ayithe credit refund (loss ledu).

Register FREE: manavivaha.in/register
Pricing: manavivaha.in/pricing
Audit: 53 privacy checks pass (e endpoint lo number leak avvadu) ✅
```
