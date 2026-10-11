# 11E — EVALUASI REVIEW EXCEL (OFFLINE, TANPA APIFY)
# Kompatibel dengan Excel asli yang ID-nya menjadi numerik, atau versi ID_FIXED.
# Selalu pulihkan ID dari CSV antrean yang dihasilkan Cell 11D.
# Tidak menimpa workbook maupun file CSV antrean.

import pandas as pd
from IPython.display import display

excel_path = REPORT_DIR / 'event_scope_v2_manual_review.xlsx'
reference_path = REPORT_DIR / 'event_scope_v2_manual_review.csv'
output_path = REPORT_DIR / 'event_scope_v2_manual_evaluation.csv'

if not excel_path.is_file() or not reference_path.is_file():
    raise FileNotFoundError('Pastikan file review .xlsx dan antrean .csv dari Cell 11D ada di folder reports.')

manual = pd.read_excel(
    excel_path,
    sheet_name='event_scope_v2_manual_review',
    dtype={'id': 'string'},
    keep_default_na=False,
    engine='openpyxl',
)
reference = pd.read_csv(reference_path, dtype={'id': 'string'}, keep_default_na=False)

key = ['case', 'created_at_source']
required_manual = set(key + ['id', 'text', 'v2_scope', 'manual_scope'])
required_ref = set(key + ['id', 'text', 'v2_scope'])
if missing := required_manual - set(manual.columns):
    raise ValueError(f'Kolom wajib Excel hilang: {sorted(missing)}')
if missing := required_ref - set(reference.columns):
    raise ValueError(f'Kolom wajib CSV hilang: {sorted(missing)}')

for df, label in [(manual, 'Excel'), (reference, 'CSV referensi')]:
    for col in key:
        df[col] = df[col].astype(str).str.strip()
    if df.duplicated(key).any():
        raise ValueError(f'Pasangan case + created_at_source tidak unik di {label}. Hentikan; perlu metode pencocokan lain.')

# Karena Excel pernah mengonversi seluruh ID panjang menjadi angka,
# pasangan kasus dan timestamp dipakai untuk mencari ID kanonis.
canonical = reference[key + ['id', 'text', 'v2_scope']].rename(
    columns={
        'id': 'id_canonical',
        'text': 'text_canonical',
        'v2_scope': 'v2_scope_canonical',
    }
)
review = manual.merge(canonical, on=key, how='left', validate='one_to_one', indicator=True)
if review['_merge'].ne('both').any():
    bad = review.loc[review['_merge'].ne('both'), key].head(5).to_dict('records')
    raise ValueError(f'Ada review Excel yang tidak ditemukan di antrean CSV: {bad}')
if review['text'].astype(str).ne(review['text_canonical'].astype(str)).any():
    raise ValueError('Teks Excel berbeda dari CSV pada salah satu timestamp. Tidak aman memulihkan ID secara otomatis.')
if review['v2_scope'].astype(str).ne(review['v2_scope_canonical'].astype(str)).any():
    raise ValueError('Kolom v2_scope berbeda dari CSV. Periksa versi audit V2 sebelum evaluasi.')

review['id_from_excel'] = review['id'].astype(str).str.strip()
review['id'] = review['id_canonical'].astype(str).str.strip()
review['id_was_changed_by_excel'] = review['id_from_excel'].ne(review['id'])

# Manual_scope milik pengguna berisi keputusan masuk/tidak masuk,
# BUKAN empat kategori event-scope. Jangan otomatis mengonversi ke empat label.
def normalize_inclusion(value):
    value = str(value or '').strip().casefold()
    if value == '':
        return ''
    if value == 'masuk ke raw data':
        return 'INCLUDE'
    if value.startswith('tidak masuk') or value.startswith('ini hanya opini'):
        return 'EXCLUDE'
    if value.upper() in {'INCLUDE', 'EXCLUDE'}:
        return value.upper()
    return 'INVALID'

review['manual_inclusion_from_text'] = review['manual_scope'].map(normalize_inclusion)
if 'manual_inclusion' in review.columns:
    chosen = review['manual_inclusion'].astype(str).str.strip().str.upper()
    review['manual_inclusion'] = chosen.where(chosen.ne(''), review['manual_inclusion_from_text'])
    conflicts = (
        chosen.ne('')
        & review['manual_inclusion_from_text'].isin(['INCLUDE', 'EXCLUDE'])
        & chosen.ne(review['manual_inclusion_from_text'])
    )
    if conflicts.any():
        raise ValueError('Kolom manual_inclusion bertentangan dengan keputusan manual_scope pada Excel.')
else:
    review['manual_inclusion'] = review['manual_inclusion_from_text']

invalid = review.loc[~review['manual_inclusion'].isin(['', 'INCLUDE', 'EXCLUDE'])]
if not invalid.empty:
    raise ValueError('Keputusan manual tidak dikenali: ' + repr(invalid['manual_scope'].unique().tolist()))

labeled = review.loc[review['manual_inclusion'].isin(['INCLUDE', 'EXCLUDE'])].copy()
print('Baris Excel:', len(review))
print('ID yang telah dipulihkan dari CSV kanonis:', int(review['id_was_changed_by_excel'].sum()))
print('Sudah direview:', len(labeled), '| Belum direview:', len(review) - len(labeled))

print('\nKeputusan manual per kasus:')
display(pd.crosstab(labeled['case'], labeled['manual_inclusion']))
print('\nPrediksi V2 vs keputusan inklusi manual:')
display(pd.crosstab(labeled['v2_scope'], labeled['manual_inclusion']))

# Kategori NEEDS_REVIEW adalah abstain, bukan prediksi EXCLUDE.
predicted = {
    'TARGET_CURRENT': 'INCLUDE',
    'TARGET_WITH_HISTORY': 'INCLUDE',
    'HISTORICAL_ONLY': 'EXCLUDE',
}
labeled['v2_binary_prediction'] = labeled['v2_scope'].map(predicted).fillna('ABSTAIN')
assessable = labeled.loc[labeled['v2_binary_prediction'].ne('ABSTAIN')].copy()
if not assessable.empty:
    assessable['match'] = assessable['v2_binary_prediction'].eq(assessable['manual_inclusion'])
    print(f'Kecocokan pada sampel berlabel dengan prediksi tegas: {assessable["match"].mean()*100:.1f}% '
          f'({assessable["match"].sum()}/{len(assessable)})')
    print('PERINGATAN: Sampel review terarah; angka ini bukan akurasi seluruh dataset.')
    print('\nKetidaksesuaian yang perlu ditinjau:')
    display(assessable.loc[~assessable['match'],
                           ['case', 'id', 'v2_scope', 'manual_inclusion', 'text', 'manual_notes']])
print('Baris V2 NEEDS_REVIEW (abstain):', int(labeled['v2_binary_prediction'].eq('ABSTAIN').sum()))

# Jika ingin menilai empat kategori event-scope, isi manual_event_scope
# sebagai label independen; keputusan INCLUDE/EXCLUDE tidak cukup untuk itu.
if 'manual_event_scope' in labeled.columns:
    m4 = labeled['manual_event_scope'].astype(str).str.strip().str.upper()
    allowed4 = {'TARGET_CURRENT', 'TARGET_WITH_HISTORY', 'HISTORICAL_ONLY', 'NEEDS_REVIEW'}
    if (~m4.isin(allowed4 | {''})).any():
        raise ValueError('Ada manual_event_scope yang bukan salah satu dari empat kelas.')
    if m4.isin(allowed4).any():
        print('\nMatriks empat kategori (hanya baris yang diberi manual_event_scope):')
        display(pd.crosstab(labeled.loc[m4.isin(allowed4), 'v2_scope'], m4[m4.isin(allowed4)]))

# Hanya tulis file evaluasi baru. Jangan edit raw, checkpoint, audit V1/V2, atau workbook manual.
review.drop(columns=['_merge', 'id_canonical', 'text_canonical', 'v2_scope_canonical']).to_csv(
    output_path, index=False, encoding='utf-8-sig'
)
print('\nEvaluasi tersimpan di:', output_path)
