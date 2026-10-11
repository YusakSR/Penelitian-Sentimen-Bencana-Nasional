# 11F — REPORT POLICY FOCUS V2.1 + KEPUTUSAN MANUAL
# Tempel sebagai code cell baru SETELAH 11E, dan jalankan OFFLINE.
# Prasyarat: Cell 06D, Cell 07, Cell 11D, Cell 11E sudah sukses.
# Periksa: Cell 11E sudah membaca workbook *_TANGGAL_FIXED.xlsx.
# Tidak mengubah V1, V2, raw, checkpoint, workbook, atau file evaluasi lama.

import pandas as pd
from IPython.display import display

v2_file = REPORT_DIR / "event_scope_v2_by_tweet.csv"
manual_file = REPORT_DIR / "event_scope_v2_manual_evaluation.csv"
if not v2_file.is_file() or not manual_file.is_file():
    raise FileNotFoundError("Butuh event_scope_v2_by_tweet.csv dan hasil Cell 11E yang diperbarui.")

v2_data = pd.read_csv(v2_file, dtype={"id": "string"}, keep_default_na=False)
review_data = pd.read_csv(manual_file, dtype={"id": "string"}, keep_default_na=False)
key = ["case", "id"]
for label, df in [("V2", v2_data), ("manual", review_data)]:
    if any(c not in df.columns for c in key):
        raise ValueError(f"Kolom case/id tidak ada di {label}.")
    for col in key:
        df[col] = df[col].astype(str).str.strip()
    if df.duplicated(key).any():
        raise ValueError(f"(case,id) duplikat di {label}.")

required_v2 = {"text", "v2_scope", "keyword_candidate"}
required_manual = {"manual_inclusion", "reviewed_at"}
if required_v2 - set(v2_data):
    raise ValueError("Kolom V2 tidak lengkap: " + str(sorted(required_v2 - set(v2_data))))
if required_manual - set(review_data):
    raise ValueError("Kolom evaluasi manual tidak lengkap: " + str(sorted(required_manual - set(review_data))))

review_data["manual_inclusion"] = review_data["manual_inclusion"].astype(str).str.strip().str.upper()
allowed = {"INCLUDE", "EXCLUDE"}
if (~review_data["manual_inclusion"].isin(allowed)).any():
    raise ValueError("Ada keputusan manual kosong/tidak valid; periksa evaluasi Excel.")

# Tanggal review diminta seragam; jangan memakai laporan Cell 11E lama.
review_dates = pd.to_datetime(review_data["reviewed_at"], errors="coerce")
if review_dates.isna().any() or not review_dates.dt.strftime("%Y-%m-%d").eq("2026-10-11").all():
    raise ValueError(
        "reviewed_at pada hasil Cell 11E belum seluruhnya 2026-10-11. "
        "Ganti excel_path ke *_TANGGAL_FIXED.xlsx dan jalankan ulang Cell 11E."
    )

review_cols = key + ["manual_inclusion", "reviewed_at"]
for col in ["manual_scope", "manual_notes", "reviewer", "manual_event_scope"]:
    if col in review_data.columns:
        review_cols.append(col)

if not set(zip(review_data.case, review_data.id)).issubset(
    set(zip(v2_data.case, v2_data.id))
):
    raise ValueError("Ada ID manual yang tidak ditemukan di dataset V2.")

result = v2_data.merge(
    review_data[review_cols], on=key, how="left", validate="one_to_one"
)
result["manual_inclusion"] = result["manual_inclusion"].fillna("")
result["reviewed_at"] = result["reviewed_at"].fillna("")

v21 = [
    classify_policy_focus_v21(x.text, x.case, x.v2_scope)
    for x in result.itertuples(index=False)
]
result["policy_focus_version"] = POLICY_FOCUS_VERSION
result["policy_focus_v21"] = [v[0] for v in v21]
result["policy_focus_reason_v21"] = [v[1] for v in v21]

# Keputusan manual hanya berlaku pada 84 tweet yang memang sudah direview.
# Belum direview TIDAK BOLEH otomatis berubah menjadi INCLUDE/EXCLUDE final.
result["final_inclusion_decision"] = result["manual_inclusion"].where(
    result["manual_inclusion"].isin(allowed), "PENDING_MANUAL"
)
convert_pred = {
    "INCLUDE_CANDIDATE": "INCLUDE",
    "EXCLUDE_CANDIDATE": "EXCLUDE",
}
result["v21_binary_suggestion"] = result["policy_focus_v21"].map(convert_pred).fillna("ABSTAIN")
result["manual_vs_v21_conflict"] = (
    result["final_inclusion_decision"].isin(allowed)
    & result["v21_binary_suggestion"].isin(allowed)
    & result["final_inclusion_decision"].ne(result["v21_binary_suggestion"])
)

summary = []
for case_id, group in result.groupby("case", sort=True):
    summary.append({
        "case": case_id,
        "unique_real_ids": len(group),
        "keyword_candidates": int(group["keyword_candidate"].astype(str).str.lower().eq("true").sum()),
        "manual_include": int(group["final_inclusion_decision"].eq("INCLUDE").sum()),
        "manual_exclude": int(group["final_inclusion_decision"].eq("EXCLUDE").sum()),
        "pending_manual": int(group["final_inclusion_decision"].eq("PENDING_MANUAL").sum()),
        "v21_include_candidate": int(group["policy_focus_v21"].eq("INCLUDE_CANDIDATE").sum()),
        "v21_exclude_candidate": int(group["policy_focus_v21"].eq("EXCLUDE_CANDIDATE").sum()),
        "v21_needs_context": int(group["policy_focus_v21"].eq("NEEDS_CONTEXT").sum()),
        "manual_vs_v21_conflict": int(group["manual_vs_v21_conflict"].sum()),
    })
summary = pd.DataFrame(summary)
conflicts = result.loc[result["manual_vs_v21_conflict"], [
    "case", "id", "text", "v2_scope", "policy_focus_v21",
    "policy_focus_reason_v21", "manual_inclusion", "reviewed_at",
]].copy()

assert len(result) == len(v2_data)
assert int(summary["unique_real_ids"].sum()) == len(v2_data)
assert int(summary[["manual_include", "manual_exclude", "pending_manual"]].sum().sum()) == len(v2_data)

csv_write_atomic(REPORT_DIR / "policy_focus_v21_by_tweet.csv", result)
csv_write_atomic(REPORT_DIR / "policy_focus_v21_by_case.csv", summary)
csv_write_atomic(REPORT_DIR / "policy_focus_v21_manual_conflicts.csv", conflicts)
print("POLICY FOCUS V2.1 — laporan offline dibuat; V1/V2 dan label manual tidak ditimpa.")
display(summary)
print("Total konflik dengan keputusan manual yang perlu ditinjau:", len(conflicts))
if not conflicts.empty:
    display(conflicts)
