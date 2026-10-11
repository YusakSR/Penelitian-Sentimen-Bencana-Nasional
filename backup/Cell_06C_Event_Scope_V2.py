# 06C — EVENT SCOPE V2 (OFFLINE; V1 TIDAK DIUBAH)
# Letakkan setelah Cell 06B dan sebelum Cell 07.
# Membutuhkan: import re, html.unescape, match_any_phrase, DISASTER_CASES,
# get_audit_event_terms(), classify_event_scope() dari Cell 06B.

from html import unescape

EVENT_SCOPE_V2_VERSION = "event_scope_v2"


def _v2_normalize(value):
    """Normalisasi hanya untuk pemeriksaan; teks asli tetap disimpan."""
    return re.sub(r"\s+", " ", unescape(str(value or "")).casefold()).strip()


def _v2_re(text, pattern):
    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def classify_event_scope_v2(text: str, case_id: str):
    """Klasifikasi heuristik konservatif; BUKAN gold-standard atau label sentimen.

    Return: (event_scope_v2, scope_reason_v2).
    """
    if case_id not in DISASTER_CASES:
        raise ValueError(f"Kasus tidak dikenali: {case_id}")

    sample = _v2_normalize(text)
    if not sample:
        return "NEEDS_REVIEW", "empty_text"

    # Periode lain tetap mengikuti V1; V2 kali ini difokuskan untuk
    # persoalan sejarah Aceh 2004 versus banjir Sumatra 2025.
    if case_id != "sumatra_2025":
        return classify_event_scope(sample, case_id)

    policy = match_any_phrase(sample, DISASTER_CASES[case_id]["policy_terms"])
    if not policy:
        return "NEEDS_REVIEW", "no_explicit_policy_term"

    locations = (
        "aceh", "sumatra", "sumatera", "sumut", "sumbar",
        "sumatera utara", "sumatra utara", "sumatera barat", "sumatra barat",
        "tapanuli", "tapteng", "taput", "tapsel", "medan", "agam",
        "aceh tamiang", "aceh utara", "langsa",
    )
    location = match_any_phrase(sample, list(locations))

    history = bool(
        _v2_re(sample, r"(?<!\w)(?:2004|1992|2006|2009|2020)(?!\w)")
        or _v2_re(sample, r"\btsunami\s+(?:aceh|sumatr[ae])\b")
        or _v2_re(sample, r"\bsumatr[ae][-\s]*andaman\b")
        or _v2_re(sample, r"\bcovid(?:[-\s]*19)?\b")
    )

    flood = _v2_re(sample, r"\b(?:banjir(?:\s+bandang)?|longsor|bencana\s+ekologis?)\b")
    explicit_year = _v2_re(sample, r"(?<!\w)2025(?!\w)")

    # Konteks tiga provinsi di Sumatra (termasuk ejaan nonbaku "propinsi").
    aceh = _v2_re(sample, r"\baceh\b")
    north = _v2_re(sample, r"\b(?:sumut|sumatr[ae]\s+utara|tapanuli|medan)\b")
    west = _v2_re(sample, r"\b(?:sumbar|sumatr[ae]\s+barat|padang|agam)\b")
    multi_region = (sum((aceh, north, west)) >= 3) or _v2_re(
        sample, r"\b(?:3|tiga)\s*(?:provinsi|propinsi)\b"
    )

    decision_action = _v2_re(
        sample,
        r"\b(?:belum|belom|blm|tidak|tdk|gak|ga|nggak|enggak|"
        r"bukan|tak\s+kunjung|mendesak|didesak|desak|minta|meminta|"
        r"dinaikkan|menaikkan|naikkan|naikin|tingkatkan|meningkatkan|"
        r"ditetapkan|menetapkan|tetapkan|penetapan|"
        r"kenapa|mengapa|perlukah|perlu|butuh|segera)\b"
    )
    now_cue = _v2_re(
        sample,
        r"\b(?:sekarang|skrg|skg|saat\s+ini|kini|hari\s+ini|"
        r"sampai\s+sekarang|hingga\s+kini|tahun\s+ini|"
        r"pemerintah\s+pusat\s+saat\s+ini|prabowo)\b"
    )
    contrasting = _v2_re(
        sample,
        r"\b(?:dulu|dlu|waktu\s+itu|zaman|jaman|"
        r"padahal|sedangkan|sementara|dibanding|beda|lah\s+ini|"
        r"kok|ko|sekarang|skrg)\b"
    )

    # Bukti kuat bahwa pembahasan menyasar bencana 2025.
    event_2025_evidence = location and (flood or explicit_year or multi_region)
    present_government = _v2_re(
        sample, r"\b(?:prabowo|pemerintah\s+pusat\s+saat\s+ini)\b"
    )
    policy_2025_evidence = location and decision_action and (multi_region or present_government)

    if history:
        if event_2025_evidence or policy_2025_evidence:
            return "TARGET_WITH_HISTORY", "2025_context_plus_history"
        if now_cue or contrasting or (location and decision_action and _v2_re(sample, r"\b(?:ini|tiga|3)\b")):
            return "NEEDS_REVIEW", "historical_comparison_ambiguous"
        return "HISTORICAL_ONLY", "historical_no_current_disaster_evidence"

    # Tanpa referensi sejarah, opini kebijakan di lokasi dan konteks
    # keputusan masa kini dapat tetap relevan meski tidak menyebut "banjir".
    if event_2025_evidence:
        return "TARGET_CURRENT", "2025_event_evidence"
    if location and decision_action:
        return "TARGET_CURRENT", "location_and_policy_decision"
    return "NEEDS_REVIEW", "insufficient_event_context"


# Unit test dari tweet nyata yang sebelumnya diperiksa.
# Ekspektasi ini adalah adjudikasi sementara untuk regresi, bukan skor akurasi.
V2_REGRESSION_SAMPLES = [
    (
        "1996005502111846540",
        "Ya Allah udh 7 hari kelaparan. Makanya rakyat minta ditetapkan bencana nasional "
        "Tsunami aceh aja dlu cm satu propinsi bisa jd bencana nasional, skrg 3 propinsi",
        "TARGET_WITH_HISTORY",
    ),
    (
        "1996594403432112336",
        "Kalo zaman SBY, hari ke 3 setelah bencana tsunami Aceh langsung tetapkan "
        "status bencana nasional. Pemerintah pusat saat ini hanya sekumpulan "
        "pengangguran yg mencari uang melalui kekuasaan @prabowo",
        "TARGET_WITH_HISTORY",
    ),
    (
        "1996207496550318418",
        "Sekarang dpr sudah mendesak status bencana nasional. Waktu tsunami aceh "
        "bisa ko, lah ini? 3 provinsi masa dibiarin",
        "TARGET_WITH_HISTORY",
    ),
    (
        "1994790454051713494",
        "Polemik Status Bencana Nasional: Perlukah Sumatera dan Aceh Dinaikkan?",
        "TARGET_CURRENT",
    ),
    (
        "1996227070318285049",
        "Saat ini berharap dinaikkan status bencana kami ini ke bencana nasional "
        "apalagi Aceh, Tapanuli, dan Sumbar",
        "TARGET_CURRENT",
    ),
    (
        "1996027810281128040",
        "Keuangan Pemda ACEH-SUMUT dan SUMBAR tidak akan mampu mengatasinya. "
        "Presiden umumkan bencana ini sebagai BENCANA NASIONAL",
        "TARGET_CURRENT",
    ),
    (
        "1996419143890018743",
        "Menurut pemerintahan Prabowo bencana Aceh Sumut Sumbar BUKAN Bencana Nasional",
        "TARGET_CURRENT",
    ),
    (
        "1996074461297344839",
        "Gempa tsunami Aceh 2004, banjir bandang longsor Aceh Sumut Sumbar 2025 "
        "mana yang diakui bencana nasional?",
        "TARGET_WITH_HISTORY",
    ),
    (
        "1996352009776304267",
        "Gempa tsunami Sumatra-Andaman 2004 dinyatakan sbg bencana nasional "
        "setelah 12 jam, jalur komunikasi Aceh terputus",
        "HISTORICAL_ONLY",
    ),
    (
        "1996265317547520148",
        "Tsunami Aceh sudah ditetapkan bencana nasional, momentum penyelesaian "
        "konflik dan perjanjian Helsinki",
        "HISTORICAL_ONLY",
    ),
    (
        "manual_ambigu",
        "Aceh 2004 dulu bencana nasional, sekarang mengapa status itu masih diperdebatkan?",
        "NEEDS_REVIEW",
    ),
    (
        "manual_non_case",
        "Status bencana nasional mungkin mengundang bantuan asing",
        "NEEDS_REVIEW",
    ),
]

for tweet_id, sample_text, expected in V2_REGRESSION_SAMPLES:
    result, reason = classify_event_scope_v2(sample_text, "sumatra_2025")
    assert result == expected, (
        f"Tweet {tweet_id}: expected {expected}; got {result} ({reason})"
    )

print(f"EVENT SCOPE V2 TEST: PASS ({len(V2_REGRESSION_SAMPLES)} kasus; tanpa Apify)")
