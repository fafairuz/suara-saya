"""Lapisan sebutan: teks sari kata -> teks yang dibaca model.
Keputusan ujian A/B (26 Nov 2026): SEMUA istilah dalam CSV ditukar ke lajur `sebutan` tanpa sengkang
(`el-el-em` -> `elelem`). Akronim yang tiada dalam CSV dieja huruf demi huruf dengan gaya yang sama.
Nombor jadi perkataan BM."""
import csv, re
from functools import lru_cache
from . import ISTILAH

HURUF = dict(A='ei', B='bii', C='sii', D='dii', E='ii', F='ef', G='jii', H='eic', I='ai', J='jei', K='kei', L='el', M='em',
             N='en', O='o', P='pii', Q='kiu', R='ar', S='es', T='tii', U='yu', V='vii', W='dabelyu', X='eks', Y='wai', Z='zed')
KLITIK = r'(?:nya|lah|kah|pun|tah)'
# sempadan perkataan: tak bersambung dengan huruf/sengkang, kecuali klitik BM (LLM-nya)
KIRI = r'(?<![\w-])'
KANAN = r'(?![\w]|-(?!' + KLITIK + r'\b))'


@lru_cache(maxsize=8)
def corak(csv_path=None):
    """[(regex, sebutan_dicantum)], terpanjang dahulu"""
    p = csv_path or str(ISTILAH); out = []
    try:
        rows = list(csv.DictReader(open(p, encoding='utf-8')))
    except FileNotFoundError:
        return []
    for r in rows:
        s = (r.get('sebutan') or '').strip()
        if not s: continue
        s = re.sub(r'\s*-\s*', '', s)                    # B: buang sengkang, cantum suku kata
        for w in {(r.get('istilah') or '').strip(), (r.get('bentuk_tulisan') or '').strip()}:
            if not w or w.lower() == s.lower(): continue
            flag = 0 if r.get('jenis') == 'AKRONIM' else re.I
            out.append((len(w), re.compile(KIRI + re.escape(w) + KANAN, flag), s))
    return [(p, s) for _, p, s in sorted(out, key=lambda x: -x[0])]


# ── nombor ───────────────────────────────────────────────────────────────────
SA = ['kosong', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'lapan', 'sembilan']


def _bawah_1000(n):
    w = []
    r, n = divmod(n, 100)
    if r: w.append('seratus' if r == 1 else SA[r] + ' ratus')
    if n >= 20:
        p, n = divmod(n, 10); w.append(SA[p] + ' puluh')
        if n: w.append(SA[n])
    elif n >= 11: w.append('sebelas' if n == 11 else SA[n - 10] + ' belas')
    elif n == 10: w.append('sepuluh')
    elif n: w.append(SA[n])
    return ' '.join(w)


def nombor(n):
    n = int(n)
    if n == 0: return 'kosong'
    w = []
    for nilai, nama in ((10 ** 9, 'bilion'), (10 ** 6, 'juta'), (1000, 'ribu')):
        q, n = divmod(n, nilai)
        if q: w.append('seribu' if (q == 1 and nama == 'ribu') else _bawah_1000(q) + ' ' + nama) if q < 1000 else w.append(nombor(q) + ' ' + nama)
    if n: w.append(_bawah_1000(n))
    return ' '.join(w)


def _angka(m):
    s = m.group(0).replace(',', '')
    if '.' in s:
        a, b = s.split('.', 1)
        return nombor(a) + ' perpuluhan ' + ' '.join(SA[int(c)] for c in b)
    return nombor(s)


def tukar_nombor(t):
    t = re.sub(r'\bke-(\d+)\b', lambda m: 'pertama' if m.group(1) == '1' else 'ke' + nombor(m.group(1)), t)
    t = re.sub(r'\bRM\s?(\d[\d,]*(?:\.\d+)?)', lambda m: _angka(re.match(r'.+', m.group(1))) + ' ringgit', t)
    t = re.sub(r'(\d[\d,]*(?:\.\d+)?)\s?%', lambda m: _angka(re.match(r'.+', m.group(1))) + ' peratus', t)
    return re.sub(r'(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.])\d+(?:\.\d+)?', _angka, t)


# ── akronim di luar CSV ──────────────────────────────────────────────────────
def eja_akronim(t):
    return re.sub(KIRI + r'[A-Z]{2,6}' + KANAN, lambda m: ''.join(HURUF[c] for c in m.group(0)), t)


def tukar(teks, csv_path=None):
    """teks sari kata -> teks_dihantar"""
    t = teks
    for p, s in corak(csv_path):
        t = p.sub(s, t)
    t = tukar_nombor(t)
    t = eja_akronim(t)
    return re.sub(r'\s+', ' ', t).strip()
