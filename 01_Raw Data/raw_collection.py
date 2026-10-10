# %% [markdown]
# # 01 — Raw Data Collection | Sentimen Kebijakan Bencana Nasional
#
# Notebook mandiri (tanpa dependensi pada file .py ini). Jalankan cell secara urut.
# **Tidak ada scraping otomatis:** `EXECUTE_SCRAPING = False` secara default.
# Raw asli disimpan sebagai JSONL; laporan kualitas tidak mengubah atau membuang raw.

# %%
# 01 — IMPORT & VERSI
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from collections import Counter
from datetime import datetime, timedelta, timezone
from getpass import getpass
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from apify_client import ApifyClient
except ImportError as exc:
    raise ImportError(
        'Paket apify-client belum terpasang. Jalankan: python -m pip install apify-client pandas'
    ) from exc

print('Pandas:', pd.__version__)
print('Import berhasil.')

# %%
# 02 — LOKASI PROJECT & OUTPUT
# Repository memiliki folder bernama "01_Raw Data" (spasi), bukan "01_Raw_Data".
# Jika Jupyter dibuka dari lokasi lain, set PROJECT_ROOT melalui environment variable.
root_env = os.getenv('PROJECT_ROOT')
if root_env:
    PROJECT_ROOT = Path(root_env).expanduser().resolve()
elif (Path.cwd() / '01_Raw Data').is_dir():
    PROJECT_ROOT = Path.cwd().resolve()
elif Path.cwd().name == '01_Raw Data':
    PROJECT_ROOT = Path.cwd().parent.resolve()
else:
    raise RuntimeError(
        'Folder 01_Raw Data tidak ditemukan. Buka notebook dari repository atau set PROJECT_ROOT.'
    )

STAGE_DIR = PROJECT_ROOT / '01_Raw Data'
OUT_DIR = STAGE_DIR / 'outputs'
RAW_DIR = OUT_DIR / 'raw_jsonl'
CSV_DIR = OUT_DIR / 'raw_csv'
AUDIT_DIR = OUT_DIR / 'audit'
STATE_DIR = OUT_DIR / 'state'
REPORT_DIR = OUT_DIR / 'reports'
for folder in [RAW_DIR, CSV_DIR, AUDIT_DIR, STATE_DIR, REPORT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

CHECKPOINT_FILE = STATE_DIR / 'collection_checkpoint.jsonl'
CONFIG_VERSION = 'policy_v2_2026_10'
ACTOR_ID = 'CJdippxWmn9uRfooo'
WIB = ZoneInfo('Asia/Jakarta')
UTC = timezone.utc

print('Project:', PROJECT_ROOT)
print('Output :', OUT_DIR)
print('Actor  :', ACTOR_ID)

# %% [markdown]
# ## Langkah 1 — Konfigurasi kasus, kata kunci, dan query
# Ketiga periode **inklusif**. Semua tanggal tweet dan jendela pengambilan dihitung dalam WIB.
# Kelompok EVENT harus berpasangan dengan kelompok POLICY. Tidak ada scraping event-only.
# Keyword luas (contohnya "status darurat", "pemerintah pusat") ditandai untuk peninjauan,
# bukan otomatis dianggap sebagai opini tentang status bencana nasional.

# %%
# 03 — KONFIGURASI PENELITIAN (dipertahankan dari notebook semula)
DISASTER_CASES = {
    'lombok_2018': {
        'label': 'Gempa Lombok 2018',
        'start_date': '2018-07-29', 'end_date': '2018-08-31',
        'pilot_date': '2018-08-06',
        'event_terms': [
            'Lombok', 'gempa Lombok', 'gempa bumi Lombok', 'gempa NTB',
            'gempa bumi NTB', 'NTB', 'Nusa Tenggara Barat', 'Mataram',
            'Lombok Utara', 'Lombok Barat', 'Lombok Timur', 'Lombok Tengah'
        ],
        'policy_terms': [
            'bencana nasional', 'status bencana nasional', 'status nasional',
            'penetapan bencana nasional', 'penetapan status bencana',
            'penetapan status', 'status bencana', 'status darurat',
            'bencana daerah', 'status bencana daerah',
            'ditetapkan sebagai bencana nasional', 'ditetapkan bencana nasional',
            'tetapkan bencana nasional', 'menetapkan bencana nasional',
            'jadi bencana nasional', 'jadiin bencana nasional'
        ],
    },
    'palu_2018': {
        'label': 'Gempa dan Tsunami Palu 2018',
        'start_date': '2018-09-28', 'end_date': '2018-10-31',
        'pilot_date': '2018-09-29',
        'event_terms': [
            'Palu', 'gempa Palu', 'gempa bumi Palu', 'tsunami Palu',
            'gempa tsunami Palu', 'Donggala', 'gempa Donggala',
            'tsunami Donggala', 'Sulawesi Tengah', 'gempa Sulawesi Tengah',
            'tsunami Sulawesi Tengah', 'bencana Palu', 'bencana Sulawesi Tengah'
        ],
        'policy_terms': [
            'bencana nasional', 'status bencana nasional', 'status nasional',
            'penetapan bencana nasional', 'penetapan status bencana',
            'penetapan status', 'status bencana', 'status darurat',
            'bencana daerah', 'status bencana daerah',
            'ditetapkan sebagai bencana nasional', 'ditetapkan bencana nasional',
            'tetapkan bencana nasional', 'menetapkan bencana nasional',
            'jadi bencana nasional', 'bantuan internasional'
        ],
    },
    'sumatra_2025': {
        'label': 'Banjir dan Longsor Sumatra 2025',
        'start_date': '2025-11-26', 'end_date': '2025-12-31',
        'pilot_date': '2025-11-29',
        'event_terms': [
            'Aceh', 'banjir Aceh', 'longsor Aceh', 'bencana Aceh',
            'Sumatra Utara', 'Sumatera Utara', 'banjir Sumatra Utara',
            'banjir Sumatera Utara', 'longsor Sumatra Utara',
            'longsor Sumatera Utara', 'bencana Sumatra Utara',
            'bencana Sumatera Utara', 'Sumatra Barat', 'Sumatera Barat',
            'banjir Sumatra Barat', 'banjir Sumatera Barat',
            'longsor Sumatra Barat', 'longsor Sumatera Barat',
            'bencana Sumatra Barat', 'bencana Sumatera Barat',
            'banjir Sumatra', 'banjir Sumatera', 'longsor Sumatra',
            'longsor Sumatera', 'bencana Sumatra', 'bencana Sumatera'
        ],
        'policy_terms': [
            'bencana nasional', 'status bencana nasional', 'status nasional',
            'penetapan bencana nasional', 'penetapan status bencana',
            'penetapan status', 'status bencana', 'status darurat',
            'bencana daerah', 'status bencana daerah',
            'ditetapkan sebagai bencana nasional', 'ditetapkan bencana nasional',
            'tetapkan bencana nasional', 'menetapkan bencana nasional',
            'jadi bencana nasional', 'prioritas nasional',
            'penanganan nasional', 'penanganan berskala nasional',
            'berskala nasional', 'ditangani pemerintah pusat',
            'penanganan pemerintah pusat', 'pemerintah pusat',
            'status daerah', 'status provinsi'
        ],
    },
}

STRONG_POLICY_TERMS = [
    'bencana nasional', 'status bencana nasional',
    'penetapan bencana nasional', 'ditetapkan sebagai bencana nasional',
    'ditetapkan bencana nasional', 'tetapkan bencana nasional',
    'menetapkan bencana nasional', 'jadi bencana nasional',
    'jadiin bencana nasional', 'status nasional'
]

BROAD_POLICY_TERMS = [
    'penetapan status bencana', 'penetapan status', 'status bencana',
    'status darurat', 'bencana daerah', 'status bencana daerah',
    'bantuan internasional', 'prioritas nasional', 'penanganan nasional',
    'penanganan berskala nasional', 'berskala nasional',
    'ditangani pemerintah pusat', 'penanganan pemerintah pusat',
    'pemerintah pusat', 'status daerah', 'status provinsi'
]

# Grup query yang sama seperti notebook lama (5 event × 6 policy / batch).
EVENT_CHUNK_SIZE = 5
POLICY_CHUNK_SIZE = 6


def chunks(items: list[str], size: int):
    if size <= 0:
        raise ValueError('Ukuran batch harus > 0')
    for i in range(0, len(items), size):
        yield items[i:i + size]


def or_query(terms: list[str]) -> str:
    return '(' + ' OR '.join('"' + term.replace('"', '') + '"' for term in terms) + ')'


def make_query_batches(case_config: dict) -> list[dict]:
    batches = []
    for e_index, events in enumerate(chunks(case_config['event_terms'], EVENT_CHUNK_SIZE), 1):
        for p_index, policies in enumerate(chunks(case_config['policy_terms'], POLICY_CHUNK_SIZE), 1):
            # X search: spasi antarkelompok bermakna konjungsi/AND.
            # Keyword kebijakan tetap diwajibkan; hindari literal 'AND' dalam kueri.
            base = f'{or_query(events)} {or_query(policies)}'
            batches.append({
                'query_id': f'E{e_index:02d}_P{p_index:02d}',
                'base_query': base,
                'event_terms': events,
                'policy_terms': policies,
            })
    return batches

for case_id, conf in DISASTER_CASES.items():
    conf['query_batches'] = make_query_batches(conf)
    print(case_id, '| event:', len(conf['event_terms']),
          '| policy:', len(conf['policy_terms']),
          '| query batch:', len(conf['query_batches']))

assert [len(DISASTER_CASES[c]['query_batches']) for c in DISASTER_CASES] == [9, 9, 24]

# %% [markdown]
# ## Langkah 2 — Query waktu dan pemeriksaan kualitas
# `lang:in` dan `since_time`/`until_time` dipilih dari hasil uji Actor sebelumnya.
# Filter waktu Actor tidak selalu konsisten; **createdAt selalu divalidasi ulang**.
# 'PASS' tidak membuktikan data lengkap atau mewakili seluruh opini publik.

# %%
# 04 — MODE EKSEKUSI, BATAS BIAYA, & ADAPTIVE
# Semua opsi produksi harus diubah secara sengaja.
RUN_MODE = 'pilot'          # 'pilot' atau 'full'
EXECUTE_SCRAPING = False   # GANTI True hanya setelah memeriksa preview
MAX_NEW_RUNS = 3           # batas banyaknya Actor call per eksekusi
MAX_ITEMS = 20             # permintaan ke actor; belum tentu batas yang dipatuhi
PILOT_QUERY_LIMIT = 1      # per kasus; 1 menghasilkan total 3 pilot task
PILOT_HOURS = 24           # dihitung sungguh-sungguh, maksimum 24 jam
PILOT_START_HOUR = 0      # jam WIB pada tanggal pilot
FULL_WINDOW_HOURS = 24    # 24 jam per jendela; ringkas biaya awal
ENABLE_ADAPTIVE = False   # aktifkan hanya setelah pilot terverifikasi
REQUEST_DELAY_SECONDS = 1.0

# Batas opsional berdasarkan pemantauan kredit; bukan estimasi biaya riil.
# Apify dapat mengembalikan data > maxItems (pada percobaan sebelumnya 40 vs 10).
# Sumber biaya sebenarnya harus diperiksa pada dashboard Apify.
MAX_ADAPTIVE_DEPTH = 3     # 24 jam -> 6 jam -> 1 jam -> 15 menit

assert RUN_MODE in {'pilot', 'full'}
assert 1 <= PILOT_HOURS <= 24 and 0 <= PILOT_START_HOUR <= 23
assert PILOT_START_HOUR + PILOT_HOURS <= 24
assert FULL_WINDOW_HOURS in {1, 6, 12, 24}
assert MAX_NEW_RUNS >= 1 and PILOT_QUERY_LIMIT >= 1


def wib_dt(day: str, hour: int = 0) -> datetime:
    return datetime.fromisoformat(day).replace(hour=hour, tzinfo=WIB)


def iso_wib(dt: datetime) -> str:
    return dt.astimezone(WIB).strftime('%Y-%m-%d %H:%M:%S%z')


def make_search_query(base_query: str, start_wib: datetime, end_wib: datetime) -> str:
    start_unix = int(start_wib.timestamp())
    end_unix = int(end_wib.timestamp())
    return f'{base_query} lang:in since_time:{start_unix} until_time:{end_unix}'


def task_key(task: dict) -> str:
    identifying = {
        'case': task['case'], 'base_query': task['base_query'],
        'start_wib': iso_wib(task['start_wib']),
        'end_wib': iso_wib(task['end_wib']),
        'config_version': CONFIG_VERSION, 'actor_id': ACTOR_ID,
    }
    digest = hashlib.sha256(
        json.dumps(identifying, sort_keys=True, ensure_ascii=False).encode('utf-8')
    ).hexdigest()[:20]
    return f"{task['case']}_{digest}"


def task_info(case_id: str, batch: dict, start: datetime, end: datetime, depth=0) -> dict:
    task = {
        'case': case_id, 'query_id': batch['query_id'],
        'base_query': batch['base_query'],
        'start_wib': start, 'end_wib': end, 'depth': depth,
    }
    task['task_id'] = task_key(task)
    task['query'] = make_search_query(task['base_query'], start, end)
    return task


def date_windows(conf: dict, hours: int):
    start = wib_dt(conf['start_date'])
    end_exclusive = wib_dt(conf['end_date']) + timedelta(days=1)
    step = timedelta(hours=hours)
    while start < end_exclusive:
        stop = min(start + step, end_exclusive)
        yield start, stop
        start = stop


def build_tasks(mode: str = RUN_MODE) -> list[dict]:
    # Round-robin antarkasus, agar batas MAX_NEW_RUNS tidak hanya
    # menghabiskan kuota untuk Lombok ketika full mode dimulai.
    case_tasks = {}
    for case_id, conf in DISASTER_CASES.items():
        group = []
        if mode == 'pilot':
            start = wib_dt(conf['pilot_date'], PILOT_START_HOUR)
            windows = [(start, start + timedelta(hours=PILOT_HOURS))]
            batches = conf['query_batches'][:PILOT_QUERY_LIMIT]
        elif mode == 'full':
            windows = list(date_windows(conf, FULL_WINDOW_HOURS))
            batches = conf['query_batches']
        else:
            raise ValueError('mode harus pilot atau full')
        for start, end in windows:
            for batch in batches:
                group.append(task_info(case_id, batch, start, end))
        case_tasks[case_id] = group

    tasks = []
    longest = max(len(group) for group in case_tasks.values())
    for index in range(longest):
        for case_id in DISASTER_CASES:
            if index < len(case_tasks[case_id]):
                tasks.append(case_tasks[case_id][index])
    return tasks


def preview_plan(mode=RUN_MODE):
    tasks = build_tasks(mode)
    print('=' * 65)
    print('PREVIEW (tidak memanggil Apify) | Mode:', mode)
    print('Config:', CONFIG_VERSION, '| Requests awal:', len(tasks))
    print('Max run baru pada satu eksekusi:', MAX_NEW_RUNS)
    for case in DISASTER_CASES:
        n = sum(t['case'] == case for t in tasks)
        print(f'  {case}: {n} task')
    print('Perkiraan biaya uang tidak dapat dihitung hanya dari jumlah task.')
    for task in tasks[:min(3, len(tasks))]:
        print('\n-', task['case'], task['query_id'])
        print(' ', iso_wib(task['start_wib']), 's/d', iso_wib(task['end_wib']))
        print(' ', task['query'])
    return tasks

TASK_PREVIEW = preview_plan()

# %%
# 05 — CEK OPERATOR & METADATA SEBELUM PANGGILAN

def preflight(tasks: list[dict]):
    assert len(DISASTER_CASES) == 3
    assert {c: len(v['query_batches']) for c, v in DISASTER_CASES.items()} == {
        'lombok_2018': 9, 'palu_2018': 9, 'sumatra_2025': 24
    }
    assert MAX_NEW_RUNS > 0
    for task in tasks:
        assert task['start_wib'] < task['end_wib']
        assert 'lang:in' in task['query']
        assert 'since_time:' in task['query'] and 'until_time:' in task['query']
        assert ' OR ' in task['base_query']
        assert ') (' in task['base_query'], 'Query harus EVENT dan POLICY'
        assert ' AND ' not in task['base_query'], 'Hapus literal AND dari query'
        assert task['case'] in DISASTER_CASES
    assert len({t['task_id'] for t in tasks}) == len(tasks)
    return True

print('Preflight:', 'PASS' if preflight(TASK_PREVIEW) else 'FAIL')

# %% [markdown]
# ## Langkah 3 — Validasi Actor, format tweet, dan pembagian jendela
# Yang divalidasi: tweet asli (`type=tweet`), ID, `createdAt` parseable, tanggal dalam jendela,
# serta dua kelompok keyword. Hasil yang meragukan tetap disimpan ke arsip raw dan audit.
# Catatan: pencocokan teks adalah indikator otomatis, bukan keputusan relevansi semantik final.

# %%
# 06 — FUNGSI AUDIT DATA (TANPA API CALL)

def match_any_phrase(text: str, terms: list[str]) -> bool:
    # Hindari pencocokan sebagian kata (misalnya 'Palu' di 'kepaluan').
    sample = str(text).casefold()
    for term in terms:
        phrase = term.casefold()
        pat = r'(?<!\w)' + re.escape(phrase) + r'(?!\w)'
        if re.search(pat, sample):
            return True
    return False


def parse_twitter_timestamp(values: pd.Series) -> pd.Series:
    result = pd.to_datetime(
        values, format='%a %b %d %H:%M:%S %z %Y',
        errors='coerce', utc=True
    )
    # Cadangan apabila format sumber suatu hari berubah.
    missing = result.isna() & values.notna()
    if missing.any():
        result.loc[missing] = pd.to_datetime(
            values.loc[missing], errors='coerce', utc=True
        )
    return result


def audit_items(items: list[dict], task: dict) -> tuple[pd.DataFrame, dict]:
    df = pd.DataFrame(items)
    initial_columns = list(df.columns)
    for column in ['type', 'id', 'createdAt', 'text', 'lang']:
        if column not in df.columns:
            df[column] = pd.Series([None] * len(df), dtype='object')

    timestamps = parse_twitter_timestamp(df['createdAt'])
    start_utc = pd.Timestamp(task['start_wib'].astimezone(UTC))
    end_utc = pd.Timestamp(task['end_wib'].astimezone(UTC))

    df['audit_created_at_utc'] = timestamps
    df['audit_is_real_tweet'] = df['type'].eq('tweet')
    df['audit_in_window'] = timestamps.ge(start_utc) & timestamps.lt(end_utc)

    # Audit menggunakan seluruh daftar istilah yang relevan dengan kasus.
    # Term yang ada dalam batch query sendiri juga wajib dicek melalui hasil.
    event_terms = DISASTER_CASES[task['case']]['event_terms']
    policy_terms = DISASTER_CASES[task['case']]['policy_terms']
    texts = df['text'].fillna('').astype(str)
    df['audit_has_event'] = texts.map(lambda x: match_any_phrase(x, event_terms))
    df['audit_has_policy'] = texts.map(lambda x: match_any_phrase(x, policy_terms))
    df['audit_policy_strong'] = texts.map(lambda x: match_any_phrase(x, STRONG_POLICY_TERMS))
    df['audit_candidate'] = (
        df['audit_is_real_tweet'] & df['audit_in_window']
        & df['audit_has_event'] & df['audit_has_policy']
    )

    valid_ids = df.loc[df['audit_is_real_tweet'], 'id'].dropna().astype(str)
    n_mock = int(df['type'].eq('mock_tweet').sum())
    n_real = int(df['audit_is_real_tweet'].sum())
    n_in = int((df['audit_is_real_tweet'] & df['audit_in_window']).sum())
    n_candidate = int(df['audit_candidate'].sum())

    metrics = {
        'rows_raw': len(df),
        'rows_real_tweet': n_real,
        'rows_mock': n_mock,
        'rows_unknown_type': int((~df['type'].isin(['tweet', 'mock_tweet'])).sum()),
        'rows_real_in_window': n_in,
        'rows_real_out_window': int((df['audit_is_real_tweet'] & ~df['audit_in_window']).sum()),
        'rows_real_missing_timestamp': int((df['audit_is_real_tweet'] & timestamps.isna()).sum()),
        'rows_event_match': int((df['audit_is_real_tweet'] & df['audit_has_event']).sum()),
        'rows_policy_match': int((df['audit_is_real_tweet'] & df['audit_has_policy']).sum()),
        'rows_event_and_policy_in_window': n_candidate,
        'rows_strong_policy_candidate': int((df['audit_candidate'] & df['audit_policy_strong']).sum()),
        'unique_real_ids': int(valid_ids.nunique()),
        'duplicate_real_ids_in_dataset': int(valid_ids.duplicated().sum()),
        'raw_columns': initial_columns,
        'created_min_utc': timestamps.min().isoformat() if timestamps.notna().any() else None,
        'created_max_utc': timestamps.max().isoformat() if timestamps.notna().any() else None,
    }
    return df, metrics


def quality_flags(metrics: dict) -> list[str]:
    flags = []
    if metrics['rows_raw'] == 0:
        flags.append('EMPTY_SEARCH')
    if metrics['rows_mock']:
        flags.append('MOCK_PRESENT')
    if metrics['rows_raw'] > 0 and metrics['rows_real_tweet'] == 0:
        flags.append('NO_REAL_TWEET')
    if metrics['rows_real_out_window']:
        flags.append('OUT_OF_WINDOW')
    if metrics['rows_real_missing_timestamp']:
        flags.append('BAD_TIMESTAMP')
    if metrics['rows_real_tweet'] and metrics['rows_event_and_policy_in_window'] == 0:
        flags.append('NO_POLICY_CANDIDATE')
    # MAX_ITEMS bukan hard-limit aktual Actor. Ini indikator risiko saja.
    if metrics['rows_raw'] >= MAX_ITEMS:
        flags.append('POSSIBLE_TRUNCATION')
    return flags or ['BASIC_CHECKS_PASS']

# Tes lokal tanpa memanggil Apify — jangan keliru sebagai tweet penelitian.
_t = TASK_PREVIEW[0]
_sample = [{'type': 'mock_tweet', 'id': 'demo', 'text': 'dummy'},
           {'type': 'tweet', 'id': 'demo-real',
            'text': 'Haruskah gempa Lombok ditetapkan sebagai bencana nasional?',
            'createdAt': 'Mon Aug 06 05:00:00 +0000 2018', 'lang': 'in'}]
_audit_demo, _m_demo = audit_items(_sample, _t)
assert _m_demo['rows_mock'] == 1 and _m_demo['rows_event_and_policy_in_window'] == 1
print('Tes fungsi audit lokal: PASS (tanpa Apify)')

# %% [markdown]
# ## Langkah 4 — Penyimpanan raw dan checkpoint
# Satu folder per kasus. JSONL mempertahankan objek tweet original, audit CSV adalah hasil turunan.
# Checkpoint memuat hash task (mempertimbangkan query dan waktu), run ID, dataset ID dan indikator kualitas.
# Task yang sudah tersimpan tidak dipanggil ulang saat notebook dijalankan ulang.

# %%
# 07 — HELPER CHECKPOINT DAN PENYIMPANAN

def json_write_atomic(path: Path, items: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False, default=str) + '\n')
    tmp.replace(path)


def csv_write_atomic(path: Path, df: pd.DataFrame):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    df.to_csv(tmp, index=False, encoding='utf-8-sig')
    tmp.replace(path)


def append_checkpoint(record: dict):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CHECKPOINT_FILE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + '\n')


def load_checkpoint() -> dict[str, dict]:
    newest = {}
    if not CHECKPOINT_FILE.exists():
        return newest
    with CHECKPOINT_FILE.open(encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RuntimeError('Checkpoint rusak. Periksa file sebelum lanjut.') from exc
            newest[entry['task_id']] = entry
    return newest


def make_run_record(task: dict, run_dict: dict, metrics: dict,
                    flags: list[str], raw_path: Path, audit_path: Path) -> dict:
    return {
        'task_id': task['task_id'], 'config_version': CONFIG_VERSION,
        'status': 'SAVED', 'case': task['case'], 'query_id': task['query_id'],
        'depth': task['depth'], 'actor_id': ACTOR_ID,
        'run_id': run_dict.get('id'),
        'dataset_id': run_dict.get('defaultDatasetId') or run_dict.get('default_dataset_id'),
        'actor_status': run_dict.get('status'),
        'query': task['query'], 'base_query': task['base_query'],
        'start_wib': iso_wib(task['start_wib']),
        'end_wib': iso_wib(task['end_wib']),
        'start_utc': task['start_wib'].astimezone(UTC).isoformat(),
        'end_utc': task['end_wib'].astimezone(UTC).isoformat(),
        'quality_flags': flags, **metrics,
        'raw_path': str(raw_path.relative_to(PROJECT_ROOT)),
        'audit_path': str(audit_path.relative_to(PROJECT_ROOT)),
        'saved_at_utc': datetime.now(UTC).isoformat(),
    }


def run_to_dict(run: Any) -> dict:
    if isinstance(run, dict):
        return run
    if hasattr(run, 'model_dump'):
        return run.model_dump(by_alias=True)
    if hasattr(run, 'to_dict'):
        return run.to_dict()
    if hasattr(run, 'default_dataset_id'):
        return {
            'default_dataset_id': run.default_dataset_id,
            'id': getattr(run, 'id', None),
            'status': getattr(run, 'status', None),
        }
    raise TypeError(f'Tipe Apify Run tidak dikenal: {type(run)}')


def get_apify_client() -> ApifyClient:
    token = os.getenv('APIFY_API_TOKEN', '').strip()
    if not token:
        token = getpass('Apify API token (tidak tampil): ').strip()
    if not token:
        raise RuntimeError('API token kosong. Tidak dapat menjalankan Actor.')
    # Jangan cetak atau simpan token dalam notebook, checkpoint, atau GitHub.
    return ApifyClient(token)

# %%
# 08 — ADAPTIVE SPLIT, DENGAN BUDGET LIMIT
# Split bukan bukti kelengkapan; hasil puncak selalu perlu ditinjau.
# ENABLE_ADAPTIVE=False secara default demi keselamatan biaya.

def split_task(task: dict) -> list[dict]:
    if task['depth'] >= MAX_ADAPTIVE_DEPTH:
        return []
    total_seconds = (task['end_wib'] - task['start_wib']).total_seconds()
    if total_seconds > 6 * 3600:
        step = timedelta(hours=6)
    elif total_seconds > 1 * 3600:
        step = timedelta(hours=1)
    elif total_seconds > 15 * 60:
        step = timedelta(minutes=15)
    else:
        return []

    result = []
    start = task['start_wib']
    while start < task['end_wib']:
        stop = min(start + step, task['end_wib'])
        # Children tetap memiliki query event+policy yang sama.
        info = {
            'query_id': task['query_id'],
            'base_query': task['base_query'],
        }
        result.append(task_info(task['case'], info, start, stop,
                                depth=task['depth'] + 1))
        start = stop
    return result

# %% [markdown]
# ## Langkah 5 — Pilot → validasi → full collection secara terkendali
# **Wajib periksa output preview sebelum mengubah EXECUTE_SCRAPING.**
# `MAX_NEW_RUNS` menjadi limit keras banyaknya `client.actor(...).call()` per eksekusi.
# Jangan anggap jendela selesai sepenuhnya bila ada `POSSIBLE_TRUNCATION`.

# %%
# 09 — WORKER (MENERIMA CLIENT, MUDAH DITEST TANPA API)

def collect_one(client, task: dict) -> dict:
    run_input = {
        'searchTerms': [task['query']],
        'maxItems': MAX_ITEMS,
        'queryType': 'Latest',
    }
    started = time.monotonic()
    run_dict = run_to_dict(client.actor(ACTOR_ID).call(run_input=run_input))
    actor_status = run_dict.get('status')
    if actor_status != 'SUCCEEDED':
        raise RuntimeError(f'Actor status: {actor_status}')

    dataset_id = run_dict.get('defaultDatasetId') or run_dict.get('default_dataset_id')
    if not dataset_id:
        raise ValueError('defaultDatasetId tidak ada dalam Run.')
    items = list(client.dataset(dataset_id).iterate_items())
    if not all(isinstance(x, dict) for x in items):
        raise TypeError('Actor mengembalikan item bukan dictionary.')

    # Simpan raw SEBELUM audit, tetap termasuk mock atau item di luar tanggal.
    raw_file = RAW_DIR / task['case'] / f"{task['task_id']}.jsonl"
    json_write_atomic(raw_file, items)
    if items:
        csv_write_atomic(CSV_DIR / task['case'] / f"{task['task_id']}.csv", pd.DataFrame(items))

    df_audit, metrics = audit_items(items, task)
    flags = quality_flags(metrics)
    audit_file = AUDIT_DIR / task['case'] / f"{task['task_id']}_audit.csv"
    csv_write_atomic(audit_file, df_audit)

    record = make_run_record(task, run_dict, metrics, flags, raw_file, audit_file)
    record['elapsed_seconds'] = round(time.monotonic() - started, 2)
    append_checkpoint(record)
    return record


def run_collection(client, mode: str = RUN_MODE,
                   max_new_runs: int = MAX_NEW_RUNS,
                   enable_adaptive: bool = ENABLE_ADAPTIVE):
    tasks = build_tasks(mode)
    preflight(tasks)
    state = load_checkpoint()
    used = 0
    failed_in_this_run = set()
    succeeded = []
    errors = []

    def visit(task):
        nonlocal used
        if used >= max_new_runs:
            return

        existing = state.get(task['task_id'])
        if existing and existing.get('status') == 'SAVED':
            record = existing
        else:
            if task['task_id'] in failed_in_this_run:
                return
            # Hard budget guard: increment SEBELUM call.
            used += 1
            print(f"\n[{used}/{max_new_runs}] {task['case']} {task['query_id']}"
                  f" | {iso_wib(task['start_wib'])} → {iso_wib(task['end_wib'])}")
            try:
                record = collect_one(client, task)
                state[task['task_id']] = record
                succeeded.append(record)
                print('  Raw:', record['rows_raw'],
                      '| In-window:', record['rows_real_in_window'],
                      '| Policy candidates:', record['rows_event_and_policy_in_window'])
                print('  Flags:', ', '.join(record['quality_flags']))
            except Exception as exc:
                # Catatan error untuk audit; retry hanya pada eksekusi berikutnya.
                failed_in_this_run.add(task['task_id'])
                entry = {
                    'task_id': task['task_id'], 'status': 'FAILED',
                    'case': task['case'], 'query': task['query'],
                    'timestamp_utc': datetime.now(UTC).isoformat(),
                    'error': f'{type(exc).__name__}: {exc}',
                }
                append_checkpoint(entry)
                state[task['task_id']] = entry
                errors.append(entry)
                print('  ERROR:', entry['error'])
                return
            finally:
                if REQUEST_DELAY_SECONDS > 0 and used < max_new_runs:
                    time.sleep(REQUEST_DELAY_SECONDS)

        # Adaptive hanya setelah raw parent tersimpan; child ditambahkan
        # bertahap dan masih tunduk pada MAX_NEW_RUNS.
        if (
            enable_adaptive
            and 'POSSIBLE_TRUNCATION' in record.get('quality_flags', [])
        ):
            for child in split_task(task):
                if used >= max_new_runs:
                    break
                visit(child)

    for task in tasks:
        if used >= max_new_runs:
            break
        visit(task)

    print('\nSELESAI: Actor calls baru:', used,
          '| Saved baru:', len(succeeded),
          '| Failed:', len(errors))
    return succeeded, errors

# %%
# 10 — GERBANG EKSEKUSI: TIDAK MENJALANKAN SCRAPING SECARA OTOMATIS
print('\nGerbang eksekusi')
print('RUN_MODE:', RUN_MODE, '| EXECUTE_SCRAPING:', EXECUTE_SCRAPING)
print('MAX_NEW_RUNS:', MAX_NEW_RUNS, '| ENABLE_ADAPTIVE:', ENABLE_ADAPTIVE)

if EXECUTE_SCRAPING:
    # Hanya meminta token ketika scraping benar-benar dimulai.
    _client = get_apify_client()
    _saved, _errors = run_collection(
        _client, mode=RUN_MODE, max_new_runs=MAX_NEW_RUNS,
        enable_adaptive=ENABLE_ADAPTIVE
    )
else:
    print('PREVIEW ONLY — tidak ada pemanggilan berbayar ke Apify.')

# %%
# 11 — LAPORAN PROGRES DAN QUALITY (bisa dijalankan tanpa scraping)

def make_collection_report():
    state = load_checkpoint()
    if not state:
        print('Belum ada checkpoint. Jalankan pilot bila siap.')
        return pd.DataFrame()
    report = pd.DataFrame(state.values())
    if 'quality_flags' in report.columns:
        report['quality_flags'] = report['quality_flags'].apply(
            lambda val: ', '.join(val) if isinstance(val, list) else str(val)
        )
    columns = [
        'case', 'query_id', 'status', 'rows_raw', 'rows_mock',
        'rows_real_in_window', 'rows_event_and_policy_in_window',
        'quality_flags', 'query', 'dataset_id', 'run_id', 'raw_path'
    ]
    for col in columns:
        if col not in report.columns:
            report[col] = None
    report = report[columns].sort_values(['case', 'query_id'], na_position='last')
    path = REPORT_DIR / 'collection_summary.csv'
    csv_write_atomic(path, report)
    print('Laporan:', path)
    print(report[['case', 'query_id', 'status', 'rows_raw',
                  'rows_real_in_window', 'rows_event_and_policy_in_window',
                  'quality_flags']].to_string(index=False, max_rows=30))
    return report

REPORT = make_collection_report()

# %%
# 12 — CONTOH TWEET KANDIDAT UNTUK TINJAUAN MANUAL (TANPA SCRAPING)
def preview_policy_samples(max_each_case=5):
    if max_each_case <= 0:
        raise ValueError('max_each_case harus > 0')
    state = load_checkpoint()
    if not state:
        print('Belum ada hasil scraping tersimpan untuk ditinjau.')
        return {}

    examples = {}
    for case_id in DISASTER_CASES:
        found = []
        for record in state.values():
            if record.get('status') != 'SAVED' or record.get('case') != case_id:
                continue
            audit_path_str = record.get('audit_path')
            if not audit_path_str:
                continue
            path = PROJECT_ROOT / audit_path_str
            if not path.is_file():
                continue
            df = pd.read_csv(path, dtype={'id': 'string'})
            if df.empty or 'audit_candidate' not in df.columns:
                continue
            good = df[
                df['audit_candidate'].astype(str).str.casefold().eq('true')
            ]
            for _, row in good.iterrows():
                found.append({
                    'id': str(row.get('id', '')),
                    'createdAt': str(row.get('createdAt', '')),
                    'text': str(row.get('text', '')),
                })
                if len(found) >= max_each_case:
                    break
            if len(found) >= max_each_case:
                break
        examples[case_id] = found
        print('\n' + '=' * 65)
        print(case_id, '| contoh kandidat otomatis:', len(found))
        for i, item in enumerate(found, 1):
            print(f"{i}. [{item['createdAt']}] {item['text'][:300]}")
        if not found:
            print('Belum ditemukan kandidat. Periksa laporan dan audit query.')
    print('\nCatatan: kandidat harus diperiksa secara semantik, bukan label final.')
    return examples

SAMPLE_TWEETS = preview_policy_samples()

# %% [markdown]
# ## Interpretasi hasil
# - `BASIC_CHECKS_PASS` = hanya lolos pemeriksaan otomatis dasar, bukan jaminan relevansi semantik/kelengkapan.
# - `NO_POLICY_CANDIDATE` = jangan langsung menganggap tidak ada opini; evaluasi operator query, rentang, dan aktor.
# - `POSSIBLE_TRUNCATION` = potensi kehilangan hasil. Setelah uji pilot, tinjau pembagian interval dan kredit.
# - `MOCK_PRESENT`, `NO_REAL_TWEET`, `OUT_OF_WINDOW` = kualitas perlu ditinjau sebelum Tahap 02.
# - `FAILED` = panggilan gagal dan dapat dicoba pada eksekusi berikutnya, tanpa mengulang task yang telah disimpan.
# - Dataset tahap 01 **bukan** training set LSTM. Tahap 02 melakukan cleaning dan Tahap 03 labeling.
#
# Untuk FULL: ubah `RUN_MODE = 'full'`, pastikan pilot telah diaudit, lalu aktifkan
# `EXECUTE_SCRAPING = True` dan tetapkan `MAX_NEW_RUNS` sesuai batas waktu/kredit.
# Jalankan ulang dari awal supaya fungsi memakai konfigurasi yang baru.
# Jangan commit folder `outputs/` atau token ke repository publik.
