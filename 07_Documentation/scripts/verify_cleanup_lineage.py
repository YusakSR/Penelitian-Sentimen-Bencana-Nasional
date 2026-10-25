"""Verify persisted research evidence. Reads files and Git objects; executes no cells.

Run with ordinary Python (not python -O). No third-party packages or network needed.
The baseline commit must be available locally. This script writes no files.
"""
from __future__ import annotations

import ast
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import symtable

ROOT = Path(__file__).resolve().parents[2]
BASE = "09391e6c5777a8c34edd8482a8bf3e2859f64408"
DECISIONS = "07_Documentation/outputs/notebook_cleanup_decisions/"
PROVENANCE = "07_Documentation/outputs/part2_provenance/"
DOC = "07_Documentation/07_documentation.ipynb"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def read_csv(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def git_blobs(tree):
    request = "".join(oid + "\n" for oid in tree.values()).encode("ascii")
    output = subprocess.check_output(
        ["git", "-C", str(ROOT), "cat-file", "--batch"], input=request
    )
    stream = io.BytesIO(output)
    blobs = {}
    for path, oid in tree.items():
        header = stream.readline().decode("ascii").split()
        require(len(header) == 3 and header[:2] == [oid, "blob"], "Missing baseline blob")
        blobs[path] = stream.read(int(header[2]))
        require(stream.read(1) == b"\n", "Invalid Git blob response")
    return blobs


def representation(data, expected):
    """Compare original bytes first; reconstructed hashes never count as exact."""
    if sha(data) == expected:
        return "EXACT_BYTES"
    if sha(data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")) == expected:
        return "CRLF_RECONSTRUCTION_ONLY"
    try:
        text = data.decode("utf-8-sig")
        output = io.StringIO(newline="")
        csv.writer(output, lineterminator="\r\n").writerows(
            csv.reader(io.StringIO(text, newline=""))
        )
        rebuilt = output.getvalue().encode("utf-8")
        if data.startswith(b"\xef\xbb\xbf"):
            rebuilt = b"\xef\xbb\xbf" + rebuilt
        if sha(rebuilt) == expected:
            return "CSV_RECORD_CRLF_RECONSTRUCTION_ONLY"
    except (UnicodeError, csv.Error):
        pass
    return "UNEXPLAINED_MISMATCH"


def module_names(source, filename):
    ast.parse(source)  # Parsing only. No exec, eval, import or notebook runner.
    table = symtable.symtable(source, filename, "exec")
    definitions = {
        value.get_name() for value in table.get_symbols()
        if value.is_assigned() or value.is_imported() or value.is_namespace()
    }

    def globals_read(scope):
        found = {
            value.get_name() for value in scope.get_symbols()
            if value.is_global() and value.is_referenced()
        }
        for child in scope.get_children():
            found.update(globals_read(child))
        return found

    reads = {value.get_name() for value in table.get_symbols() if value.is_referenced()}
    reads.update(globals_read(table))
    return definitions, reads


def verify():
    # Pin the complete source set, rather than trusting only a subset of hashes.
    tree = {}
    for entry in git("ls-tree", "-rz", BASE).split(b"\0"):
        if entry:
            meta, path = entry.split(b"\t", 1)
            tree[path.decode("utf-8")] = meta.decode().split()[2]
    require(len(tree) == 464, "Unexpected baseline source set")
    baseline_bytes = git_blobs(tree)
    ledger = read_csv(DECISIONS + "source_integrity.csv")
    require(len(ledger) == len(tree), "Source integrity ledger incomplete")
    require({row["path"] for row in ledger} == set(tree), "Baseline paths differ")
    unchanged = 0
    for row in ledger:
        path = row["path"]
        before = baseline_bytes[path]
        after = (ROOT / path).read_bytes()
        require(row["baseline_commit"] == BASE, "Incorrect source baseline")
        require(row["git_blob_oid"] == tree[path], "Incorrect Git blob reference: " + path)
        require(sha(before) == row["before_sha256"], "Incorrect baseline SHA: " + path)
        require(sha(after) == row["after_sha256"], "Current source SHA differs: " + path)
        if path != DOC:
            require(before == after, "Protected source changed: " + path)
            unchanged += 1
    old_doc = json.loads(baseline_bytes[DOC].decode("utf-8"))
    new_doc = read_json(DOC)
    require(new_doc["cells"][:len(old_doc["cells"])] == old_doc["cells"],
            "Original documentation cells/outputs/metadata changed")
    require({k: v for k, v in new_doc.items() if k != "cells"} ==
            {k: v for k, v in old_doc.items() if k != "cells"}, "Notebook metadata changed")
    added = new_doc["cells"][len(old_doc["cells"]):]
    require(len(added) == 3 and all(c["cell_type"] == "markdown" for c in added),
            "Only three Markdown cells may be appended")
    require([c["id"] for c in added] == ["cleanup-review-20261025", "diagnostics-guide-20261025", "part2-lineage-20261025"],
            "Unexpected added documentation cells")

    inventory = read_csv("07_Documentation/outputs/notebook_cleanup_preflight/notebook_cell_inventory.csv")
    matrix = read_csv(DECISIONS + "cleanup_decision_matrix.csv")
    reconciliation = read_csv(DECISIONS + "preflight_cell_reconciliation.csv")
    candidates = [r for r in inventory if r["recommendation"] in ("REVIEW", "OPTIONAL")]
    key = lambda r: (r["notebook"], int(r["cell_index"]))
    require(len(inventory) == 238 and len(matrix) == 81 and len(reconciliation) == 238,
            "Cell coverage differs")
    require(Counter(r["recommendation"] for r in candidates) == {"REVIEW": 80, "OPTIONAL": 1},
            "Preflight classifications differ")
    require(len({key(r) for r in matrix}) == 81 and {key(r) for r in matrix} == {key(r) for r in candidates},
            "Decision matrix missing/duplicate cells")
    nbs = {p: read_json(p) for p in tree if p.endswith(".ipynb")}
    for row in inventory + matrix + reconciliation:
        c = nbs[row["notebook"]]["cells"][int(row["cell_index"]) - 1]
        source = "".join(c["source"])
        require(sha(source.encode("utf-8")) == row["source_sha256"], "Cell source differs: " + str(key(row)))
        require(c.get("id", "") == row["cell_id"], "Cell ID differs: " + str(key(row)))
    require(Counter(r["disposition"] for r in matrix) == {
        "KEEP_PIPELINE": 18, "KEEP_CONTEXT": 9, "KEEP_HISTORICAL": 48,
        "DIAGNOSTIC_EXPLAINED": 4, "OPTIONAL_EXPLAINED": 2,
    }, "Unexpected dispositions")
    require(all(r["review_status"] == "STATIC_SOURCE_REVIEW_COMPLETE_HUMAN_PR_REVIEW_PENDING" for r in matrix),
            "Human review must remain pending")
    graph = []
    for path, nb in nbs.items():
        symbols = {}
        for i, c in enumerate(nb["cells"], 1):
            symbols[i] = module_names("".join(c["source"]), path) if c["cell_type"] == "code" else (set(), set())
        for target in symbols:
            for source in range(1, target):
                common = symbols[source][0] & symbols[target][1]
                if common:
                    graph.append((path, source, target, ";".join(sorted(common))))
    recorded_graph = [(r["notebook"], int(r["source_cell"]), int(r["target_cell"]), r["shared_names"])
                      for r in read_csv(DECISIONS + "refreshed_cell_dependencies.csv")]
    require(sorted(graph) == sorted(recorded_graph), "Static dependency graph differs")

    historical = read_csv(DECISIONS + "historical_sha_checks.csv")
    snapshot_recovered = False
    for row in historical:
        data = baseline_bytes[row["path"]]
        require(sha(data) == row["git_bytes_sha256"], "Historical Git bytes differ")
        status = representation(data, row["expected_sha256"])
        if row["status"] == "SELF_SNAPSHOT_FULL_HASH_DIFF_SOURCE_CELLS_MATCH":
            require(row["path"] == DOC and status == "UNEXPLAINED_MISMATCH", "Unexpected self snapshot exception")
            snapshot = json.loads(baseline_bytes[DOC].decode("utf-8"))
            snapshot["cells"][1]["outputs"] = []
            snapshot["cells"][1]["execution_count"] = None
            recovered_bytes = (json.dumps(snapshot, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
            require(sha(recovered_bytes) == row["expected_sha256"], "Documentation self snapshot cannot be recovered")
            snapshot_recovered = True
        else:
            require(status == row["status"] and status != "UNEXPLAINED_MISMATCH", "Historical SHA check failed: " + row["path"])
    require(Counter(r["status"] for r in historical) == {
        "EXACT_BYTES": 114, "CRLF_RECONSTRUCTION_ONLY": 327,
        "CSV_RECORD_CRLF_RECONSTRUCTION_ONLY": 139, "SELF_SNAPSHOT_FULL_HASH_DIFF_SOURCE_CELLS_MATCH": 1,
    }, "Historical hash coverage differs")
    manifest = read_csv(PROVENANCE + "source_manifest.csv")
    for row in manifest:
        require(row["git_blob_oid"] == tree[row["path"]] and
                sha((ROOT / row["path"]).read_bytes()) == row["git_bytes_sha256"], "Part2 source changed")

    p = {
        "master": "01_Raw Data/outputs/reports/batch7/final_collection/master_tweets_current.csv",
        "rawinv": "01_Raw Data/outputs/reports/batch7/final_collection/raw_inventory_current.csv",
        "eligible": "01_Raw Data/outputs/reports/batch7/manual_reconciliation/Batch7_Eligible_Tweets.csv",
        "excluded": "01_Raw Data/outputs/reports/batch7/manual_reconciliation/Batch7_Excluded_Tweets.csv",
        "clean381": "02_Cleaning/outputs/reconciliation/part8_content_reconciled.csv",
        "clean348": "02_Cleaning/outputs/reconciliation/part8_model_candidates.csv",
        "input381": "03_Labeling/inputs/labeling_all_381.csv",
        "input348": "03_Labeling/inputs/labeling_candidates_348.csv",
        "final381": "03_Labeling/outputs/final_labeling/labeled_final_381.csv",
        "final348": "03_Labeling/outputs/final_labeling/modeling_labeled_348.csv",
        "adjudicated": "04_Modeling/outputs/label_adjudication/modeling_labeled_348_adjudicated.csv",
        "grouped": "04_Modeling/outputs/leakage_grouping/modeling_labeled_348_grouped.csv",
    }
    data = {k: read_csv(path) for k, path in p.items()}
    indices = {k: {r["id"]: r for r in records} for k, records in data.items() if k != "rawinv"}
    for k, records in indices.items():
        require(len(records) == len(data[k]), "Duplicate IDs: " + k)
    master_ids = set(indices["master"])
    eligible = set(indices["eligible"])
    excluded = set(indices["excluded"])
    selected = set(indices["final348"])
    require(len(master_ids) == 411 and len(eligible) == 381 and len(excluded) == 30,
            "Raw/review counts differ")
    require(not eligible & excluded and eligible | excluded == master_ids, "Manual review partition differs")
    for k in ("clean381", "input381", "final381"):
        require(set(indices[k]) == eligible, "381 ID set differs: " + k)
    for k in ("clean348", "input348", "adjudicated", "grouped"):
        require(set(indices[k]) == selected, "348 ID set differs: " + k)
    require(len(selected) == 348 and selected < eligible, "Selection differs")
    require({i for i, r in indices["clean381"].items() if r["eligible_for_model_candidate"].lower() == "true"} == selected,
            "Eligibility flags differ")
    require(Counter(r["model_selection_status"] for r in data["clean381"]) == {
        "SELECTED_UNIQUE": 327, "SELECTED_REPRESENTATIVE": 21, "GROUP_MEMBER_NOT_SELECTED": 33,
    }, "Duplicate selection counts differ")
    for i in eligible:
        require(indices["master"][i]["text"] == indices["eligible"][i]["text"] == indices["clean381"][i]["text_original"],
                "Original text differs: " + i)
        require(indices["clean381"][i]["text_linguistic"] == indices["input381"][i]["text_linguistic"],
                "Full handoff text differs: " + i)
    require(all(not r["sentiment_label"] for r in data["input381"] + data["input348"]), "Input labels no longer blank")

    raw = {}
    raw_metadata = {}
    totals = Counter()
    ids = set()
    aggregate = hashlib.sha256()
    inventory_hash = {r["path"]: r["expected_sha256"] for r in historical
                      if r["evidence"].endswith("repository_inventory.csv")}
    for record in sorted(data["rawinv"], key=lambda r: r["task_id"]):
        path = record["raw_path"].replace("\\", "/")
        records = [json.loads(line) for line in (ROOT / path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        raw[path] = records
        raw_metadata[path] = record
        types = Counter(r["type"] for r in records)
        require(len(records) == int(record["raw_rows"]) and types["tweet"] == int(record["tweet_rows"]) and
                types["mock_tweet"] == int(record["mock_rows"]), "Raw inventory differs: " + path)
        require(set(types) <= {"tweet", "mock_tweet"}, "Unexpected raw record type")
        totals.update({"raw": len(records), "tweet": types["tweet"], "mock": types["mock_tweet"]})
        ids.update(str(r["id"]) for r in records if r["type"] == "tweet")
        aggregate.update(record["task_id"].encode("utf-8"))
        aggregate.update(inventory_hash[path].encode("ascii"))
    require(len(raw) == 65 and totals == {"raw": 1508, "tweet": 989, "mock": 519} and ids == master_ids,
            "Raw totals/unique IDs differ")
    require(aggregate.hexdigest() == read_json("01_Raw Data/outputs/reports/batch7/final_collection/current_manifest.json")["raw_manifest_sha256"],
            "Historical aggregate raw hash differs")
    for i, record in indices["master"].items():
        path = record["raw_path"].replace("\\", "/")
        payload = raw[path][int(record["raw_line_number"]) - 1]
        require(str(payload["id"]) == i and payload["type"] == "tweet" and payload["text"] == record["text"],
                "Raw master record pointer differs: " + i)
        require(all(record[field] == raw_metadata[path][field] for field in ("case", "task_id", "run_id")),
                "Raw master task/run/case differs from raw inventory: " + i)

    lineage = read_csv(PROVENANCE + "observation_lineage_348.csv")
    require(len(lineage) == 348 and {r["id"] for r in lineage} == selected, "Observation coverage differs")
    rownums = {k: {r["id"]: n for n, r in enumerate(records, 1)} for k, records in data.items() if k != "rawinv"}
    pointer_fields = {"master": "master_record", "eligible": "eligible_record", "clean381": "clean381_record",
                      "clean348": "clean348_record", "input348": "labeling_input_record", "final381": "labeling_final381_record",
                      "final348": "labeling_final348_record", "grouped": "modeling_grouped_record"}
    changed = set()
    for row in lineage:
        i = row["id"]
        source = indices["final348"][i]
        model = indices["grouped"][i]
        master = indices["master"][i]
        require(row["raw_path"] == master["raw_path"].replace("\\", "/") and
                row["raw_line_number"] == master["raw_line_number"] and row["raw_task_id"] == master["task_id"] and
                row["raw_run_id"] == master["run_id"], "Raw pointer metadata differs")
        require(row["raw_git_sha256"] == sha((ROOT / row["raw_path"]).read_bytes()), "Raw SHA differs")
        require(row["raw_created_at"] == raw[row["raw_path"]][int(row["raw_line_number"]) - 1]["createdAt"], "Raw timestamp differs")
        for k, field in pointer_fields.items():
            require(int(row[field]) == rownums[k][i], "Record pointer differs: " + field)
        for k in indices:
            if i in indices[k]:
                require(indices[k][i]["case"] == row["case"], "Case differs: " + i)
        for k in ("clean381", "clean348", "input381", "input348", "final381", "adjudicated", "grouped"):
            require(indices[k][i]["text_linguistic"] == source["text_linguistic"], "Model text differs: " + i)
        require(sha(source["text_linguistic"].encode("utf-8")) == source["final_text_hash"] == row["final_text_hash"] == model["final_text_hash"],
                "Text hash differs: " + i)
        require(indices["input348"][i]["final_text_hash"] == row["final_text_hash"], "Input hash differs")
        require(indices["final381"][i]["sentiment_label"] == source["sentiment_label"] == row["label_phase03"], "Phase03 label differs")
        require(indices["adjudicated"][i]["sentiment_label"] == model["sentiment_label"] == row["label_phase04"], "Phase04 label differs")
        require(row["annotation_source_recorded"] == source["annotation_source"] and
                row["duplicate_group_id"] == source["duplicate_group_id"] and row["leakage_group_id"] == model["leakage_group_id"],
                "Group/annotation metadata differs")
        diff = source["sentiment_label"] != model["sentiment_label"]
        require(row["phase04_label_changed"] == str(diff), "Label change flag differs")
        if diff:
            changed.add(i)
    changelog = read_csv("04_Modeling/outputs/label_adjudication/label_adjudication_changelog.csv")
    require(changed == {r["id"] for r in changelog if r["adjudication_decision"] == "CHANGE"} ==
            {"1027914286184550402", "1046787140594618373"}, "Modeling changes differ from adjudication log")
    for row in changelog:
        require(indices["final348"][row["id"]]["sentiment_label"] == row["previous_label"] and
                indices["grouped"][row["id"]]["sentiment_label"] == row["final_label"], "Changelog label mismatch")
    label_counts = Counter(r["sentiment_label"] for r in data["final348"])
    model_counts = Counter(r["sentiment_label"] for r in data["grouped"])
    require(label_counts == {"NETRAL": 223, "POSITIF": 110, "NEGATIF": 15} and
            model_counts == {"NETRAL": 225, "POSITIF": 108, "NEGATIF": 15}, "Label distributions differ")
    require(Counter(r["case"] for r in data["final348"]) == {"lombok_2018": 101, "palu_2018": 105, "sumatra_2025": 142},
            "Case distribution differs")
    require(len({r["leakage_group_id"] for r in data["grouped"]}) == 337, "Leakage group count differs")

    ai = read_csv("03_Labeling/outputs/hybrid_labeling/ai_predictions_251.csv")
    pending = read_csv("03_Labeling/outputs/hybrid_labeling/ai_pending_251.csv")
    manual = read_csv("03_Labeling/outputs/hybrid_labeling/manual_locked_130.csv")
    pending_ids = {r["id"] for r in pending}
    manual_ids = {r["id"] for r in manual}
    require(len(ai) == 10 and len(pending) == len(pending_ids) == 251 and len(manual) == len(manual_ids) == 130,
            "Hybrid evidence counts differ")
    require(not pending_ids & manual_ids and pending_ids | manual_ids == eligible and {r["id"] for r in ai} <= pending_ids,
            "Hybrid ID partition differs")
    issues = read_json("06_Result/outputs/integrated_report/open_methodological_issues.json")
    require(len(issues["issues"]) == 4 and all(not i["resolved"] for i in issues["issues"]), "Methodological issues changed")

    # Check the authored package after scientific checks, including this verifier.
    artifacts = read_json("07_Documentation/outputs/review_artifact_sha256.json")
    for path, expected in artifacts["sha256"].items():
        require(sha((ROOT / path).read_bytes()) == expected, "Review artifact SHA differs: " + path)
    return {
        "status": "PASS_WITH_DOCUMENTED_PROVENANCE_GAP",
        "baseline_commit": BASE,
        "baseline_files_checked": len(tree),
        "protected_files_byte_identical": unchanged,
        "original_cells_source_and_id_verified": len(inventory),
        "candidate_cells_reviewed": len(matrix),
        "research_and_backup_notebooks_byte_identical": 9,
        "appended_documentation_markdown_cells": len(added),
        "historical_sha_checks": dict(Counter(r["status"] for r in historical)),
        "preflight_documentation_self_snapshot_sha_recovered": snapshot_recovered,
        "raw_records": dict(totals),
        "observations_traced_to_raw": len(lineage),
        "phase03_labels": dict(label_counts),
        "phase04_labels": dict(model_counts),
        "additional_modeling_label_changes": sorted(changed),
        "ai_prediction_rows_present": len(ai),
        "provenance_gap": "No complete AI prediction/acceptance review log for the 251 pending rows",
        "existing_methodological_issues_open": 4,
        "academic_status": "PROVISIONAL",
        "research_cells_executed": 0,
        "files_written_by_verifier": 0,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
