# 📱 CHANNEL CREATE LIST — ఇది చూసి ఒక్కొక్కటి create చేయండి

**మొత్తం 52 channels** — కానీ ఒకేసారి అన్నీ వద్దు. **దశ (wave) ప్రకారం** చేయండి.
ప్రతి channel ki: **Name copy → Username copy → Description paste → @telugumatrimony1_bot ni admin**

## ⚡ ఒక్కో channel ki 4 నిమిషాలు (phone lo)
1. Telegram → ☰ → **New Channel** → Name (క్రింద టేబుల్ నుంచి copy) → **Public** → Username (copy)
2. Description paste (kit file లో ఉంది — `channel-kits/<key>.md`) → Create
3. Channel → **Administrators** → Add Admin → `@telugumatrimony1_bot` → Change Info + Post + Edit + Pin ✅
4. `python setup_channels.py --apply --key <key>` → title/desc/DP/📌 pinned అన్నీ ఆటో సెట్

**Username already taken అయితే?** → పక్కన fallback username వాడండి (అదే పని చేస్తుంది).

## 🌊 Wave 1 — మొదటి దశ (వెంటనే చేయండి) (20 channels)

| # | Name (copy) | Username (copy) | Fallback | Status |
|---|---|---|---|---|
| 1 | `📢 TSAP Matrimony Official \| మన వివాహ — TS-AP` | `@TSAP_MATRIMONY` | @manavivaha, @manavivaha_official | ⬜ create |
| 2 | `👰 AP Brides \| ఆంధ్రా వధువులు` | `@APBRIDE` | @manavivaha_ap_bride, @apbride1 | ⬜ create |
| 3 | `🤵 AP Grooms \| ఆంధ్రా వరులు` | `@APGROOM1` | @manavivaha_ap_groom, @apgroom | ⬜ create |
| 4 | `👰 TS Brides \| తెలంగాణ వధువులు` | `@TSBRIDE` | @manavivaha_ts_bride, @tsbrides | ✅ LIVE |
| 5 | `🤵 TS Grooms \| తెలంగాణ వరులు` | `@TSGROOM1` | @manavivaha_ts_groom, @tsgroom | ✅ LIVE |
| 6 | `👰 Kamma Brides \| కమ్మ వధువులు` | `@manavivaha_kamma_bride` | @tsap_kamma_bride, @mv_kamma_brd | ⬜ create |
| 7 | `🤵 Kamma Grooms \| కమ్మ వరులు` | `@manavivaha_kamma_groom` | @tsap_kamma_groom, @mv_kamma_grm | ⬜ create |
| 8 | `👰 Kapu • Balija • Telaga Brides \| కాపు • బలిజ • తెలగ వధువులు` | `@manavivaha_kapu_bride` | @tsap_kapu_bride, @mv_kapu_brd | ⬜ create |
| 9 | `🤵 Kapu • Balija • Telaga Grooms \| కాపు • బలిజ • తెలగ వరులు` | `@manavivaha_kapu_groom` | @tsap_kapu_groom, @mv_kapu_grm | ⬜ create |
| 10 | `👰 Reddy Brides \| రెడ్డి వధువులు` | `@manavivaha_reddy_bride` | @tsap_reddy_bride, @mv_reddy_brd | ⬜ create |
| 11 | `🤵 Reddy Grooms \| రెడ్డి వరులు` | `@manavivaha_reddy_groom` | @tsap_reddy_groom, @mv_reddy_grm | ⬜ create |
| 12 | `✝️ AP Christian Brides \| ఆంధ్రా క్రైస్తవ వధువులు` | `@manavivaha_christian_ap_bride` | @apchristianbride, @mv_christ_ap_brd | ⬜ create |
| 13 | `✝️ AP Christian Grooms \| ఆంధ్రా క్రైస్తవ వరులు` | `@manavivaha_christian_ap_groom` | @apchristiangroom, @mv_christ_ap_grm | ⬜ create |
| 14 | `✝️ Telangana Christian Brides \| తెలంగాణ క్రైస్తవ వధువులు` | `@manavivaha_christian_ts_bride` | @tschristianbride, @mv_christ_ts_brd | ⬜ create |
| 15 | `✝️ Telangana Christian Grooms \| తెలంగాణ క్రైస్తవ వరులు` | `@manavivaha_christian_ts_groom` | @tschristiangroom, @mv_christ_ts_grm | ⬜ create |
| 16 | `🕉️ Hindu Matrimony \| హిందూ వివాహాలు` | `@manavivaha_hindu` | @manavivaha_hindus, @tsap_hindu | ⬜ create |
| 17 | `☪️ AP Muslim Brides \| ఆంధ్రా ముస్లిం వధువులు` | `@manavivaha_muslim_ap_bride` | @apmuslimbride, @mv_muslim_ap_brd | ⬜ create |
| 18 | `☪️ AP Muslim Grooms \| ఆంధ్రా ముస్లిం వరులు` | `@manavivaha_muslim_ap_groom` | @apmuslimgroom, @mv_muslim_ap_grm | ⬜ create |
| 19 | `☪️ Telangana Muslim Brides \| తెలంగాణ ముస్లిం వధువులు` | `@manavivaha_muslim_ts_bride` | @tsmuslimbride, @mv_muslim_ts_brd | ⬜ create |
| 20 | `☪️ Telangana Muslim Grooms \| తెలంగాణ ముస్లిం వరులు` | `@manavivaha_muslim_ts_groom` | @tsmuslimgroom, @mv_muslim_ts_grm | ⬜ create |

### ✅ Wave-1 ayyaka ee command run cheyyandi

```bash
export BOT_TOKEN=xxxx
python setup_channels.py --apply --wave 1 --mark-live
python setup_channels.py --check          # anni perfect ఉన్నాయా చూడండి
```

## 🌊 Wave 2 — రెండో దశ (17 channels)

| # | Name (copy) | Username (copy) | Fallback | Status |
|---|---|---|---|---|
| 1 | `🌍 NRI Telugu Matrimony \| విదేశీ సంబంధాలు` | `@manavivaha_nri` | @manavivaha_global, @manavivaha_usa | ⬜ create |
| 2 | `👰 Brahmin Brides \| బ్రాహ్మణ వధువులు` | `@manavivaha_brahmin_bride` | @tsap_brahmin_bride, @mv_brahmin_brd | ⬜ create |
| 3 | `🤵 Brahmin Grooms \| బ్రాహ్మణ వరులు` | `@manavivaha_brahmin_groom` | @tsap_brahmin_groom, @mv_brahmin_grm | ⬜ create |
| 4 | `👰 Madiga Brides \| మాదిగ వధువులు` | `@manavivaha_madiga_bride` | @tsap_madiga_bride, @mv_madiga_brd | ⬜ create |
| 5 | `🤵 Madiga Grooms \| మాదిగ వరులు` | `@manavivaha_madiga_groom` | @tsap_madiga_groom, @mv_madiga_grm | ⬜ create |
| 6 | `👰 Mala Brides \| మాల వధువులు` | `@manavivaha_mala_bride` | @tsap_mala_bride, @mv_mala_brd | ⬜ create |
| 7 | `🤵 Mala Grooms \| మాల వరులు` | `@manavivaha_mala_groom` | @tsap_mala_groom, @mv_mala_grm | ⬜ create |
| 8 | `💍 Munnuru Kapu Matrimony \| మున్నూరు కాపు — వధువులు + వరులు` | `@manavivaha_munnuru_kapu` | @tsap_munnuru_kapu, @manavivaha_munnuru_kapu_community | ⬜ create |
| 9 | `👰 Velama Brides \| వెలమ వధువులు` | `@manavivaha_velama_bride` | @tsap_velama_bride, @mv_velama_brd | ⬜ create |
| 10 | `🤵 Velama Grooms \| వెలమ వరులు` | `@manavivaha_velama_groom` | @tsap_velama_groom, @mv_velama_grm | ⬜ create |
| 11 | `💍 Viswabrahmana (Viswakarma) Matrimony \| విశ్వబ్రాహ్మణ — వధువులు + వరులు` | `@manavivaha_viswabrahmana` | @tsap_viswabrahmana, @manavivaha_viswabrahmana_community | ⬜ create |
| 12 | `👰 Arya Vysya • Komati Brides \| వైశ్య • కోమటి వధువులు` | `@manavivaha_vysya_bride` | @tsap_vysya_bride, @mv_vysya_brd | ⬜ create |
| 13 | `🤵 Arya Vysya • Komati Grooms \| వైశ్య • కోమటి వరులు` | `@manavivaha_vysya_groom` | @tsap_vysya_groom, @mv_vysya_grm | ⬜ create |
| 14 | `👰 Yadava • Goud • Golla Brides \| యాదవ • గౌడ • గొల్ల వధువులు` | `@manavivaha_yadava_goud_bride` | @tsap_yadava_goud_bride, @mv_yadava_goud_brd | ⬜ create |
| 15 | `🤵 Yadava • Goud • Golla Grooms \| యాదవ • గౌడ • గొల్ల వరులు` | `@manavivaha_yadava_goud_groom` | @tsap_yadava_goud_groom, @mv_yadava_goud_grm | ⬜ create |
| 16 | `🕊️ Other Religions \| ఇతర మత వివాహాలు` | `@manavivaha_other_religions` | @manavivaha_others, @manavivaha_minority | ⬜ create |
| 17 | `💍 Second Marriage \| రెండో పెళ్లి` | `@manavivaha_second` | @tsap_second, @manavivaha_remarriage | ⬜ create |

## 🌊 Wave 3 — మూడో దశ (15 channels)

| # | Name (copy) | Username (copy) | Fallback | Status |
|---|---|---|---|---|
| 1 | `💍 Lambada • Banjara (ST) Matrimony \| లంబాడ • బంజార — వధువులు + వరులు` | `@manavivaha_lambada_banjara` | @tsap_lambada_banjara, @manavivaha_lambada_banjara_community | ⬜ create |
| 2 | `💍 Mudiraj • Tenugollu Matrimony \| ముదిరాజ • తెనుగొల్ల — వధువులు + వరులు` | `@manavivaha_mudiraj` | @tsap_mudiraj, @manavivaha_mudiraj_community | ⬜ create |
| 3 | `💍 Other BC Communities Matrimony \| ఇతర BC కులాలు — వధువులు + వరులు` | `@manavivaha_others_bc` | @tsap_others_bc, @manavivaha_others_bc_community | ⬜ create |
| 4 | `💍 Other SC Communities Matrimony \| ఇతర SC కులాలు — వధువులు + వరులు` | `@manavivaha_others_sc` | @tsap_others_sc, @manavivaha_others_sc_community | ⬜ create |
| 5 | `💍 Other ST Communities Matrimony \| ఇతర ST కులాలు — వధువులు + వరులు` | `@manavivaha_others_st` | @tsap_others_st, @manavivaha_others_st_community | ⬜ create |
| 6 | `💍 Padmashali • Devanga (Weavers) Matrimony \| పద్మశాలి • దేవాంగ — వధువులు + వరులు` | `@manavivaha_padmashali_weavers` | @tsap_padmashali_weavers, @manavivaha_padmashali_weavers_community | ⬜ create |
| 7 | `💍 Raju • Kshatriya Matrimony \| రాజు • క్షత్రియ — వధువులు + వరులు` | `@manavivaha_raju_kshatriya` | @tsap_raju_kshatriya, @manavivaha_raju_kshatriya_community | ⬜ create |
| 8 | `💞 Inter-Faith & Love \| ప్రేమ వివాహాలు` | `@manavivaha_interfaith` | @manavivaha_intercaste, @manavivaha_mixedmarriage | ⬜ create |
| 9 | `🤝 Bureau / Broker Network \| బ్రోకర్ల నెట్‌వర్క్` | `@manavivaha_bureau` | @tsap_bureau, @manavivaha_brokers | ⬜ create |
| 10 | `♿ Differently-Abled \| ప్రత్యేక సామర్థ్యం` | `@manavivaha_able` | @tsap_handicapped, @manavivaha_differentlyabled | ⬜ create |
| 11 | `🩺 Doctors & Teachers Matrimony \| వైద్యులు + ఉపాధ్యాయులు` | `@manavivaha_professionals` | @manavivaha_doctors, @tsap_doctors | ⬜ create |
| 12 | `🚨 Fraud Alerts \| మోసం జాగ్రత్త` | `@manavivaha_alerts` | @tsap_alerts | ⬜ create |
| 13 | `🏛️ Govt Jobs Matrimony \| ప్రభుత్వ ఉద్యోగులు` | `@manavivaha_govt` | @tsap_govt, @manavivaha_govtjobs | ⬜ create |
| 14 | `💻 Software Matrimony \| సాఫ్ట్‌వేర్ ఉద్యోగులు` | `@manavivaha_software` | @tsap_software, @manavivaha_it | ⬜ create |
| 15 | `🏆 Success Stories \| విజయ గాథలు` | `@manavivaha_success` | @tsap_success | ⬜ create |

## 🎯 ముఖ్యమైన సూచనలు

- **Wave-1 = 17 channels** (Official + 4 main + 6 castes × bride/groom) — ఇవి ముందు చేయండి
- ఒకేసారి 20+ channels create చేయకండి (Telegram 'Too Many Attempts' ఇస్తుంది) → 10 చేసి 1 గంట ఆగండి
- **@TSBRIDE / @TSGROOM1** ఇప్పటికే ఉన్నాయి — వాటికి bot admin ఉందో ఒకసారి check చేయండి
- AP channels: `@APBRIDE`, `@APGROOM1` (India motham lo ఎవరూ తీసుకోకుండా ముందే పెట్టేయండి)
- Caste channels: top 6 castes → Reddy, Kamma, Kapu, Velama, Vysya, Brahmin (bride + groom separate)
