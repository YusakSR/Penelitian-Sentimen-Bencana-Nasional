# 11D — EVENT SCOPE V2: LAPORAN, PERBANDINGAN V1, DAN REVIEW MANUAL
# Letakkan setelah Cell 11C. Jalankan saat EXECUTE_SCRAPING == False.
# Input: event_scope_v1_by_tweet.csv (TIDAK ditimpa).
from IPython.display import display
import hashlib


def report_event_scope_v2():
    v1_file = REPORT_DIR / "event_scope_v1_by_tweet.csv"
    if not v1_file.is_file():
        raise FileNotFoundError(
            "Laporan V1 tidak ditemukan. Jalankan Cell 11C (OFFLINE) lebih dahulu."
        )

    df = pd.read_csv(
        v1_file, dtype={"id": "string"}, keep_default_na=False
    )
    needed = {
        "case", "id", "text", "keyword_candidate", "event_scope",
        "scope_reason", "task_id", "run_id",
    }
    if missing := needed - set(df.columns):
        raise ValueError(f"Kolom wajib V1 hilang: {sorted(missing)}")
    if df.duplicated(["case", "id"]).any():
        raise ValueError("File V1 memiliki duplikasi (case, id). Periksa sebelum lanjut.")

    # Simpan hasil V1 persis sebagai basis perbandingan; jangan tulis ulang CSV V1.
    df = df.rename(columns={
        "event_scope": "v1_scope", "scope_reason": "v1_reason"
    }).copy()
    df["keyword_candidate"] = (
        df["keyword_candidate"].astype(str).str.lower().eq("true")
    )
    df["v2_version"] = EVENT_SCOPE_V2_VERSION

    v2 = [
        classify_event_scope_v2(row.text, row.case)
        for row in df.itertuples(index=False)
    ]
    df["v2_scope"] = [x[0] for x in v2]
    df["v2_reason"] = [x[1] for x in v2]
    df["v1_to_v2_changed"] = df["v1_scope"].ne(df["v2_scope"])

    # Tambah waktu unggahan dari audit asli berdasarkan (case, id).
    # V1 tetap apa adanya; raw/checkpoint/audit asli tidak ditimpa.
    state = load_checkpoint()
    created_at = {}
    missing_audits = []
    for task in state.values():
        if task.get("status") != "SAVED":
            continue
        path = task.get("audit_path")
        if not path:
            missing_audits.append(str(task.get("task_id")))
            continue
        audit_file = PROJECT_ROOT / Path(str(path).replace("\\", "/"))
        if not audit_file.is_file():
            missing_audits.append(str(audit_file))
            continue
        source = pd.read_csv(
            audit_file,
            dtype={"id": "string"},
            keep_default_na=False,
            usecols=lambda c: c in ("id", "type", "createdAt"),
        )
        if not {"id", "type", "createdAt"}.issubset(source.columns):
            raise ValueError(f"Kolom id/type/createdAt hilang: {audit_file}")
        for row in source.loc[source["type"].eq("tweet")].itertuples(index=False):
            key = (str(task["case"]), str(row.id).strip())
            if key not in created_at and str(row.createdAt).strip():
                created_at[key] = str(row.createdAt)

    if missing_audits:
        raise RuntimeError(
            f"{len(missing_audits)} audit historis hilang; "
            f"contoh: {missing_audits[:2]}"
        )

    df["created_at_source"] = [
        created_at.get((str(row.case), str(row.id)), "")
        for row in df.itertuples(index=False)
    ]

    # Ringkasan hanya untuk tweet yang lolos keyword V1 (agar sebanding).
    cand = df.loc[df["keyword_candidate"]].copy()
    cases = list(DISASTER_CASES)
    summary = []
    for case in cases:
        group = cand.loc[cand["case"].eq(case)]
        all_case = df.loc[df["case"].eq(case)]
        counts = group["v2_scope"].value_counts()
        summary.append({
            "case": case,
            "unique_real": len(all_case),
            "keyword_candidates": len(group),
            "target_current": int(counts.get("TARGET_CURRENT", 0)),
            "target_with_history": int(counts.get("TARGET_WITH_HISTORY", 0)),
            "historical_only": int(counts.get("HISTORICAL_ONLY", 0)),
            "needs_review": int(counts.get("NEEDS_REVIEW", 0)),
            "event_relevant_auto": int(
                counts.get("TARGET_CURRENT", 0)
                + counts.get("TARGET_WITH_HISTORY", 0)
            ),
            "changed_vs_v1": int(group["v1_to_v2_changed"].sum()),
        })
    by_case = pd.DataFrame(summary)

    transitions = (
        cand.groupby(["case", "v1_scope", "v2_scope"], dropna=False)
        .size().reset_index(name="n_tweets")
        .sort_values(["case", "v1_scope", "v2_scope"])
    )

    assert len(df) == df[["case", "id"]].drop_duplicates().shape[0]
    assert int(by_case["unique_real"].sum()) == len(df)
    assert int(by_case["keyword_candidates"].sum()) == len(cand)
    assert (by_case[[
        "target_current", "target_with_history", "historical_only", "needs_review"
    ]].sum(axis=1) == by_case["keyword_candidates"]).all()

    # Simpan V2 dengan nama baru; JANGAN overwrite V1.
    csv_write_atomic(REPORT_DIR / "event_scope_v2_by_tweet.csv", df)
    csv_write_atomic(REPORT_DIR / "event_scope_v2_by_case.csv", by_case)
    csv_write_atomic(REPORT_DIR / "event_scope_v2_transitions.csv", transitions)

    # Review prioritas: semua ambigu/historis/perubahan dari V1.
    # Tambah kontrol deterministik ~20% dari label yang tidak berubah,
    # untuk memeriksa false positive yang lolos di kedua versi.
    queue_path = REPORT_DIR / "event_scope_v2_manual_review.csv"
    priority_mask = (
        cand["v2_scope"].isin(["NEEDS_REVIEW", "HISTORICAL_ONLY"])
        | cand["v1_to_v2_changed"]
    )
    unchanged_target = cand["v2_scope"].isin([
        "TARGET_CURRENT", "TARGET_WITH_HISTORY"
    ]) & ~cand["v1_to_v2_changed"]
    sample_unchanged = pd.Series([
        int(hashlib.sha256(
            f"{r.case}:{r.id}".encode("utf-8")
        ).hexdigest()[:8], 16) % 5 == 0
        for r in cand.itertuples(index=False)
    ], index=cand.index)
    queue_mask = priority_mask | (unchanged_target & sample_unchanged)
    queue = cand.loc[queue_mask, [
        "case", "id", "created_at_source", "text", "v1_scope", "v2_scope",
        "v2_reason", "v1_to_v2_changed",
    ]].copy()
    queue["review_stratum"] = [
        "priority" if priority_mask.loc[i] else "sample_unchanged"
        for i in queue.index
    ]
    queue["manual_scope"] = ""
    queue["manual_notes"] = ""
    queue["reviewer"] = ""
    queue["reviewed_at"] = ""
    if queue_path.exists():
        prev = pd.read_csv(queue_path, dtype={"id": "string"}, keep_default_na=False)
        if prev.duplicated(["case", "id"]).any():
            raise ValueError("Ada ID ganda dalam antrean review lama.")
        old_ids = set(zip(prev["case"].astype(str), prev["id"].astype(str)))
        fresh = queue.loc[[
            (str(r.case), str(r.id)) not in old_ids
            for r in queue.itertuples(index=False)
        ]]
        # Baris lama tidak diubah agar label dan catatan manual aman.
        queue = pd.concat([prev, fresh], ignore_index=True)
    csv_write_atomic(queue_path, queue)

    display(by_case)
    display(transitions)
    print("ID unik asli:", len(df))
    print("Kandidat keyword:", len(cand))
    print("Relevan otomatis V2:", int(by_case["event_relevant_auto"].sum()))
    print("Berubah dari V1:", int(cand["v1_to_v2_changed"].sum()))
    print("Antrean review (termasuk label yang sudah dikerjakan):", len(queue))
    return df, by_case, transitions, queue


df_scope_v2, df_scope_v2_case, df_scope_v2_transitions, df_scope_v2_review = report_event_scope_v2()
