# 11E — EVALUASI REVIEW MANUAL (OPSIONAL, OFFLINE)
# Isi "manual_scope" terlebih dahulu pada event_scope_v2_manual_review.csv
# dengan salah satu kategori: TARGET_CURRENT, TARGET_WITH_HISTORY,
# HISTORICAL_ONLY, NEEDS_REVIEW.
from IPython.display import display

review_path = REPORT_DIR / "event_scope_v2_manual_review.csv"
review_df = pd.read_csv(review_path, dtype={"id": "string"}, keep_default_na=False)
allowed = {"TARGET_CURRENT", "TARGET_WITH_HISTORY", "HISTORICAL_ONLY", "NEEDS_REVIEW"}
invalid = review_df.loc[
    review_df["manual_scope"].ne("") & ~review_df["manual_scope"].isin(allowed)
]
if len(invalid):
    raise ValueError("Nilai manual_scope tidak valid: " + ", ".join(invalid["manual_scope"].unique()))

labeled = review_df.loc[review_df["manual_scope"].isin(allowed)].copy()
print("Sudah direview:", len(labeled), "/", len(review_df))

if not labeled.empty:
    print("Matriks prediksi V2 (baris) versus keputusan manual (kolom):")
    display(pd.crosstab(
        labeled["v2_scope"], labeled["manual_scope"],
        rownames=["V2"], colnames=["Manual"]
    ))
    print("Persentase kecocokan pada sampel berlabel:",
          round(100 * labeled["v2_scope"].eq(labeled["manual_scope"]).mean(), 1), "%")
    print("Catatan: persentase ini bukan akurasi seluruh dataset (sampel review dipilih secara terarah).")
else:
    print("Belum ada label manual. Ini normal sebelum tahap review.")
