"""Portal uji suara (halaman /uji pada pelayan perakam): taip atau ambil ayat rawak, jana dengan satu atau lebih
tetapan, dengar, nilai. Model dimuat sekali (bila pertama kali diperlukan) dan kekal dalam memori pelayan.
Ayat rawak tak guna AI: ia diambil dari CSV/skrip sedia ada, atau templat BM yang diisi istilah dari CSV."""
import csv, json, random, re, threading, time, uuid
from datetime import datetime
from pathlib import Path
from . import D, KERJA
from .sebutan import tukar
from .bank import baca
from .persona import dapat, senarai as senarai_persona, lalai as persona_lalai

UJI = KERJA / 'uji'
LOG = UJI / 'log.jsonl'
PRASET = [
    dict(nama='lalai', cfg=0.3, ex=0.5, suhu=0.5, ket='tetapan enjin sekarang (varian3)'),
    dict(nama='lama', cfg=0.5, ex=0.5, suhu=0.7, ket='tetapan lalai sebelum 27 Nov 2026'),
    dict(nama='cfg0', cfg=0.0, ex=0.5, suhu=0.7, ket='kurang tiru gaya rujukan'),
    dict(nama='tenang', cfg=0.5, ex=0.3, suhu=0.5, ket='kurang ekspresif'),
]
TEMPLAT = [
    "Jadi, sebelum {a} dihantar, sistem semak {b} dulu.",
    "Cuma {a} yang dipercayai boleh masuk ke {b}.",
    "Kalau {a} gagal, pasukan kena semak {b} secara manual.",
    "Data dalam {a} tu tak boleh dipalsukan, sebab ada {b}.",
    "Sebenarnya {a} ni mudah je, macam {b} tapi lebih telus.",
    "Kita guna {a} untuk pastikan {b} sentiasa selamat dan berintegriti.",
    "Sistem ni proses {n} rekod sehari, semuanya melalui {a}.",
    "Dalam fasa kedua, kita akan tambah {a} dan uji {b} dengan pengguna sebenar.",
    "Berapa lama masa yang diperlukan untuk {a} siap?",
    "Kenapa {a} perlu disambungkan terus ke {b}?",
]
_kunci = threading.Lock()
_E = None


def _csv_semua():
    for p in sorted(D.glob('*.csv')):
        try:
            yield from csv.DictReader(open(p, encoding='utf-8'))
        except Exception:
            continue


def ayat_rawak(mod='ayat'):
    if mod == 'templat':
        ist = list({r['bentuk_tulisan'] or r['istilah'] for r in _csv_semua() if r.get('jenis') in ('EN', 'AKRONIM')})
        a, b = random.sample(ist, 2)
        return random.choice(TEMPLAT).format(a=a, b=b, n=random.choice([12, 250, 1500, 32000, 1200000]))
    kolam = {r['contoh_ayat'].strip() for r in _csv_semua() if r.get('contoh_ayat', '').strip()}
    for p in D.glob('skrip*.md'):
        tajuk = ''
        for b in open(p, encoding='utf-8'):
            if b.startswith('#'): tajuk = b.lower(); continue
            if 'arahan' not in tajuk and (m := re.match(r'^\s*\d+[.)]\s+(.+)$', b)): kolam.add(re.sub(r'[*_`]', '', m.group(1)).strip())
    return random.choice(sorted(kolam))


def senarai_rujukan(persona=None):
    """pilihan klip rujukan persona: auto, rujukan/*.flac, ambilan ayat dalam bank"""
    P = dapat(persona)
    r = [dict(nilai='', label='auto (ikut gaya)')]
    r += [dict(nilai=P.rel(q), label=f'rujukan/{q.name}') for q in sorted(P.rujukan.glob('*.flac'))]
    for a in baca(P)['ambilan']:
        if a['jenis'] == 'ayat' and (P.bank / a['fail']).exists():
            r.append(dict(nilai=P.rel(P.bank / a['fail']), label=f"bank/{a['fail']} ({a['tempoh']} s, {round((a.get('skor_whisper') or 0) * 100)}%)"))
    return r


def mula(persona=None):
    from .rakam import senarai_gaya
    P = dapat(persona)
    return dict(praset=PRASET, persona=senarai_persona(), persona_dipilih=P.nama, gaya=senarai_gaya(P.nama), rujukan=senarai_rujukan(P.nama),
                model_dimuat=_E is not None, sejarah=sejarah())


def sejarah(n=30):
    if not LOG.exists(): return []
    rows = [json.loads(l) for l in open(LOG, encoding='utf-8') if l.strip()]
    nilai = {r['id']: r for r in rows if r.get('jenis') == 'nilai'}
    out = [dict(r, nilai=nilai.get(r['id'], {}).get('nilai'), nota=nilai.get(r['id'], {}).get('nota')) for r in rows if r.get('jenis') == 'jana']
    return out[::-1][:n]


def jana(J):
    """J: {teks, persona?, gaya, rujukan?, praset:[{nama,cfg,ex,suhu}], benih, semak}"""
    global _E
    import numpy as np, soundfile as sf
    teks = (J.get('teks') or '').strip()
    if not teks: raise ValueError('teks kosong')
    if len(teks) > 600: raise ValueError('teks terlalu panjang (had 600 aksara untuk ujian)')
    from .enjin import pecah_ayat
    UJI.mkdir(parents=True, exist_ok=True); hasil = []
    with _kunci:                                          # satu jana pada satu masa (GPU)
        t0 = time.time()
        P = dapat(J.get('persona'))
        ruj = None
        if J.get('rujukan'):
            ruj = (D / J['rujukan']).resolve()
            if not ruj.is_relative_to(P.dir): raise ValueError('klip rujukan mesti dari persona yang sama')
        if _E is None:
            from .enjin import Enjin
            _E = Enjin(J.get('gaya') or 'santai', persona=P.nama)
        muat_s = round(time.time() - t0, 1)
        for p in J.get('praset') or PRASET[:1]:
            _E.guna(J.get('gaya') or 'santai', p.get('ex'), ruj, P.nama)
            t1 = time.time(); bahagian = []; ayat = []
            for s in pecah_ayat(teks):
                w, dihantar, sk, h, b = _E.satu(s, int(J.get('benih', 7)), semak=bool(J.get('semak', True)), cfg=p.get('cfg'), suhu=p.get('suhu'))
                bahagian += [w.astype(np.float32), np.zeros(int(0.35 * _E.sr), np.float32)]
                ayat.append(dict(teks=s, teks_dihantar=dihantar, skor=sk, didengar=h, benih=b))
            y = np.concatenate(bahagian[:-1]); y = y / max(1e-6, np.abs(y).max()) * 0.89
            i = uuid.uuid4().hex[:10]; f = UJI / f'{i}.flac'; sf.write(f, y, _E.sr)
            sk = [a['skor'] for a in ayat if a['skor'] is not None]
            r = dict(jenis='jana', id=i, tarikh=datetime.now().isoformat(timespec='seconds'), teks=teks, persona=P.nama, gaya=_E.gaya, rujukan=_E.ket,
                     praset=p.get('nama', 'sendiri'), cfg=p.get('cfg'), ex=_E.ex, suhu=p.get('suhu'), fail=f'kerja/uji/{i}.flac',
                     tempoh=round(len(y) / _E.sr, 1), masa_jana=round(time.time() - t1, 1), skor=min(sk) if sk else None, ayat=ayat)
            with open(LOG, 'a', encoding='utf-8') as fo: fo.write(json.dumps(r, ensure_ascii=False) + '\n')
            hasil.append(r)
    return dict(hasil=hasil, muat_model_s=muat_s)


def nilai(J):
    UJI.mkdir(parents=True, exist_ok=True)
    r = dict(jenis='nilai', id=J['id'], nilai=J.get('nilai'), nota=(J.get('nota') or '')[:500], tarikh=datetime.now().isoformat(timespec='seconds'))
    with open(LOG, 'a', encoding='utf-8') as fo: fo.write(json.dumps(r, ensure_ascii=False) + '\n')
    return {'ok': True}


def sebut(teks):
    return dict(teks_dihantar=tukar(teks))
