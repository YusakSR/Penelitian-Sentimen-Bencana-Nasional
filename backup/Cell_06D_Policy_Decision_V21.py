# 06D — AUDIT FOKUS PENETAPAN STATUS NASIONAL (V2.1, OFFLINE)
# Sisipkan setelah Cell 06C. Biarkan fungsi dan laporan V1/V2 apa adanya.
# Ini menilai fokus kebijakan, BUKAN mengganti event_scope V2 atau label manual.

import re
from html import unescape

POLICY_FOCUS_VERSION = "policy_focus_v2_1"


def _pf21_norm(value):
    return re.sub(r"\s+", " ", unescape(str(value or "")).casefold()).strip()


def _pf21_has(text, regex):
    return bool(re.search(regex, text, flags=re.IGNORECASE))


def classify_policy_focus_v21(text, case_id, v2_scope=""):
    """Return (policy_focus_v21, focus_reason_v21).

    INCLUDE_CANDIDATE = berbicara tentang penetapan/penolakan status nasional
                        dan memiliki bukti peristiwa target.
    EXCLUDE_CANDIDATE = tak membahas keputusan status / bukan peristiwa target.
    NEEDS_CONTEXT     = perlu konteks thread / anotasi manual, jangan dibuang.
    """
    t = _pf21_norm(text)
    if not t:
        return "NEEDS_CONTEXT", "empty_text"
    if case_id not in ("lombok_2018", "palu_2018", "sumatra_2025"):
        raise ValueError(f"Unknown case: {case_id}")

    national_status = _pf21_has(
        t,
        r"\b(?:bencana\s+nasional|status\s+(?:bencana\s+)?nasional|"
        r"status\s+bencana|status\s+darurat)\b",
    )
    decision_action = _pf21_has(
        t,
        r"\b(?:status|penetap\w*|menetap\w*|ditetap\w*|tetap\w*|"
        r"netap\w*|netep\w*|menaik\w*|dinaik\w*|naikkan|naikin|"
        r"ditingkat\w*|meningkat\w*|menjadi|dijadi\w*|jadikan|"
        r"dinyata\w*|menyata\w*|deklarasi|dideklarasi\w*|diumum\w*|"
        r"menolak|ditolak|bukan|belum|belom|tidak\s+masuk\s+kriteria|"
        r"ga\s+jadi|gak\s+jadi|nggak\s+jadi)\b",
    )
    # Konteks penolakan eksplisit dengan gaya informal: "bencana nasional, ya ga lah".
    denial_after_status = _pf21_has(
        t,
        r"\bbencana\s+nasional\W{0,8}(?:ya\s+)?(?:ga|gak|nggak|enggak|tidak|bukan)\b",
    )
    if not national_status:
        return "EXCLUDE_CANDIDATE", "no_national_status_discussion"
    # Berita bencana semata bukan pembahasan penetapan status; pengecualian
    # eksplisit berikut menghindari homonim/metafora bencana nasional.
    if _pf21_has(t, r"\bkorupsi\b.{0,60}\bbencana\s+nasional\b") and not decision_action:
        return "EXCLUDE_CANDIDATE", "metaphor_not_national_disaster_decision"
    if _pf21_has(t, r"\bmemimpin\s+penangg?ulangan\s+bencana\s+nasional\b") and not decision_action:
        return "EXCLUDE_CANDIDATE", "leadership_of_response_not_status_decision"
    if not (decision_action or denial_after_status):
        # 'bencana nasional' tanpa verba penetapan tidak cukup untuk
        # otomatis ditolak: bisa berupa diskusi status atau judul artikel.
        return "NEEDS_CONTEXT", "national_disaster_phrase_without_clear_decision"

    if case_id != "sumatra_2025":
        terms = (
            ["Lombok", "NTB", "Nusa Tenggara Barat"] if case_id == "lombok_2018"
            else ["Palu", "Donggala", "Sulteng", "Sulawesi Tengah"]
        )
        at_target = any(_pf21_has(t, r"(?<!\w)" + re.escape(x.casefold()) + r"(?!\w)") for x in terms)
        if at_target:
            return "INCLUDE_CANDIDATE", "explicit_target_and_status_decision"
        return "NEEDS_CONTEXT", "national_status_without_target_event"

    # Aceh 2004 tidak boleh otomatis diartikan sebagai banjir/longsor 2025.
    historical = _pf21_has(
        t,
        r"(?<!\w)(?:2004|1992|2006|2009|2020)(?!\w)|"
        r"\b(?:tsunami\s+aceh|tsunami\s+sumatr[ae]|sumatr[ae][\s-]*andaman|covid)\b",
    )
    location = _pf21_has(
        t,
        r"\b(?:aceh|sumatr[ae]|sumut|sumbar|tapanuli|tapteng|taput|"
        r"tapsel|medan|padang|agam|langsa)\b",
    )
    present_disaster = _pf21_has(
        t, r"\b(?:banjir|longsor|banjir\s+bandang|bencana\s+ekologis?)\b"
    )
    year_target = _pf21_has(t, r"(?<!\w)2025(?!\w)")
    aceh = _pf21_has(t, r"\baceh\b")
    north = _pf21_has(t, r"\b(?:sumut|sumatr[ae]\s+utara|tapanuli|medan)\b")
    west = _pf21_has(t, r"\b(?:sumbar|sumatr[ae]\s+barat|padang|agam)\b")
    multiregion = (int(aceh) + int(north) + int(west) >= 2) or _pf21_has(
        t, r"\b(?:3|tiga)\s*(?:provinsi|propinsi)\b"
    )
    present_cue = _pf21_has(
        t, r"\b(?:sekarang|skrg|skg|saat ini|hingga kini|hari ini|tahun ini|lah ini)\b"
    )
    # Dua provinsi Aceh+Sumut pada uraian tsunami 2004 tidak otomatis
    # membuktikan ada pembahasan banjir 2025.
    target_evidence = location and (
        present_disaster or year_target
        or (multiregion and (not historical or present_cue))
    )
    if target_evidence:
        return "INCLUDE_CANDIDATE", (
            "target_2025_with_historical_comparison" if historical
            else "target_2025_status_decision"
        )
    if historical:
        # Daftar statis kejadian lama tanpa target 2025 / ajakan membandingkan.
        if _pf21_has(t, r"\b(?:1992|2004)\b") and _pf21_has(t, r"\b2020\b") and not _pf21_has(
            t, r"\b(?:sekarang|skrg|saat ini|kini|lah ini|masa|kok|ko|padahal|banding)\b"
        ):
            return "EXCLUDE_CANDIDATE", "static_history_list_no_target_2025"
        # Beberapa tweet membandingkan pemerintah masa kini vs 2004, tetapi
        # tidak menyebut banjir 2025; jangan paksa INCLUDE maupun EXCLUDE.
        return "NEEDS_CONTEXT", "historical_without_explicit_2025_event"
    if location:
        # Dalam arsip 2025 hal ini mungkin terkait bencana target, tetapi
        # membutuhkan konteks lebih kuat sebelum diperlakukan sebagai fakta.
        return "NEEDS_CONTEXT", "place_and_status_without_2025_event_anchor"
    return "NEEDS_CONTEXT", "status_without_identifiable_target_event"


# UJI REGRESI — teks asli 6 kasus review vs V2 (bukan pelatihan model).
# Dua 'manual INCLUDE' historis sengaja diarahkan ke NEEDS_CONTEXT,
# bukan dipaksa menjadi peristiwa Sumatra 2025.
POLICY_FOCUS_V21_TESTS = [
    ("lombok_2018", "Korupsi itu baru bencana nasional kl yg di Lombok itu bencana alam", "EXCLUDE_CANDIDATE"),
    ("palu_2018", "Presiden harus memimpin penanggulangan Bencana Nasional di Palu", "EXCLUDE_CANDIDATE"),
    ("lombok_2018", "Gempa kembali mengguncang Lombok dan korban meninggal", "EXCLUDE_CANDIDATE"),
    ("sumatra_2025", "Bencana nasional, ya ga lah. Tsunami Aceh dan gempa Yogya dulu", "NEEDS_CONTEXT"),
    ("sumatra_2025", "Pemerintah netapin bencana nasional baru tsunami Aceh dan covid; bencana Palu tidak", "NEEDS_CONTEXT"),
    ("sumatra_2025", "Waktu tsunami Aceh SBY tetapkan status bencana nasional; pemerintah pusat saat ini berbeda", "NEEDS_CONTEXT"),
    ("sumatra_2025", "Banjir Aceh Sumut Sumbar 2025 belum ditetapkan bencana nasional", "INCLUDE_CANDIDATE"),
    ("palu_2018", "PKS desak status bencana nasional bagi gempa Palu", "INCLUDE_CANDIDATE"),
]
for _case, _text, _expected in POLICY_FOCUS_V21_TESTS:
    _got, _reason = classify_policy_focus_v21(_text, _case)
    assert _got == _expected, (_case, _expected, _got, _reason)
print(f"POLICY FOCUS V2.1: PASS ({len(POLICY_FOCUS_V21_TESTS)} skenario; offline)")
