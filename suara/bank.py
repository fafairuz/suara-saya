"""Bank suara: bank/manifest.json dan pemilihan klip rujukan untuk setiap gaya."""
import json, re, threading, unicodedata
from datetime import datetime
from . import BANK, GAYA, KERJA, D
from .sebutan import corak

MANIFEST = BANK / 'manifest.json'
_kunci = threading.Lock()


def slug(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60] or 'x'


def baca():
    if MANIFEST.exists():
        return json.load(open(MANIFEST, encoding='utf-8'))
    return dict(versi=1, ambilan=[])


def tulis(M):
    BANK.mkdir(parents=True, exist_ok=True)
    tmp = MANIFEST.with_suffix('.tmp'); json.dump(M, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); tmp.replace(MANIFEST)


def tambah(rekod, pilihan=True):
    """tambah satu ambilan; jika pilihan, nyahpilih ambilan lain bagi (slug, gaya, jenis) yang sama"""
    with _kunci:
        M = baca()
        if pilihan:
            for a in M['ambilan']:
                if (a['slug'], a['gaya'], a['jenis']) == (rekod['slug'], rekod['gaya'], rekod['jenis']): a['pilihan'] = False
        rekod['pilihan'] = pilihan; rekod.setdefault('tarikh', datetime.now().isoformat(timespec='seconds'))
        M['ambilan'].append(rekod); tulis(M)
    return rekod


def ambilan_seterusnya(slug_, gaya, jenis):
    n = [a['ambilan'] for a in baca()['ambilan'] if (a['slug'], a['gaya'], a['jenis']) == (slug_, gaya, jenis)]
    return max(n, default=0) + 1


# ── klip rujukan ─────────────────────────────────────────────────────────────
def _kaya_istilah(teks):
    return sum(1 for p, _ in corak() if p.search(teks))


def rujukan(gaya):
    """(laluan klip, keterangan). Susunan: gaya/<gaya>.json -> klip terbaik bank (8–12 s) ->
    gabungan ambilan ayat terbaik sehingga ~10 s -> rujukan/<gaya>.flac -> rujukan/santai.flac"""
    f = GAYA / f'{gaya}.json'
    if f.exists():
        g = json.load(open(f, encoding='utf-8'))
        if g.get('rujukan'):
            p = (D / g['rujukan']).resolve()
            if p.exists(): return p, f'tetap: {g["rujukan"]}'
    calon = [a for a in baca()['ambilan'] if a['gaya'] == gaya and a['jenis'] == 'ayat' and a.get('skor_whisper', 0) >= 0.9
             and not a.get('amaran') and (BANK / a['fail']).exists()]
    nilai = lambda a: a['skor_whisper'] + 0.05 * _kaya_istilah(a['teks'])
    tepat = sorted([a for a in calon if 8 <= a['tempoh'] <= 12], key=nilai, reverse=True)
    if tepat: return BANK / tepat[0]['fail'], f'bank: {tepat[0]["fail"]}'
    if calon:
        pilih, jum = [], 0.0
        for a in sorted(calon, key=nilai, reverse=True):
            if jum >= 9: break
            pilih.append(a); jum += a['tempoh'] + 0.3
        if jum >= 6: return _gabung(gaya, pilih), f'gabungan {len(pilih)} ambilan bank ({jum:.0f} s)'
    for n in (gaya, 'santai'):
        p = D / 'rujukan' / f'{n}.flac'
        if p.exists(): return p, f'lalai: rujukan/{n}.flac'
    raise SystemExit('Tiada klip rujukan. Rakam bank (bin/suara rakam) atau letak rujukan/santai.flac')


def _gabung(gaya, pilih):
    import numpy as np, soundfile as sf
    KERJA.mkdir(exist_ok=True); out = KERJA / f'rujukan-{gaya}.flac'
    bahagian = []
    for a in pilih:
        y, sr = sf.read(BANK / a['fail'], dtype='float32'); bahagian += [y, np.zeros(int(0.3 * sr), np.float32)]
    sf.write(out, np.concatenate(bahagian[:-1]), sr); return out
