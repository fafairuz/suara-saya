"""Bank suara setiap persona: persona/<nama>/bank/manifest.json dan pemilihan klip rujukan untuk setiap gaya."""
import json, re, threading, unicodedata
from datetime import datetime
from . import KERJA, D
from .sebutan import corak
from .persona import Persona, dapat

_kunci = threading.Lock()


def slug(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60] or 'x'


def _p(p):
    return p if isinstance(p, Persona) else dapat(p)


def baca(p=None):
    p = _p(p)
    if p.manifest.exists():
        return json.load(open(p.manifest, encoding='utf-8'))
    return dict(versi=1, persona=p.nama, ambilan=[])


def tulis(p, M):
    p = _p(p); p.bank.mkdir(parents=True, exist_ok=True)
    tmp = p.manifest.with_suffix('.tmp'); json.dump(M, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); tmp.replace(p.manifest)


def tambah(p, rekod, pilihan=True):
    """tambah satu ambilan; jika pilihan, nyahpilih ambilan lain bagi (slug, gaya, jenis) yang sama"""
    p = _p(p)
    with _kunci:
        M = baca(p)
        if pilihan:
            for a in M['ambilan']:
                if (a['slug'], a['gaya'], a['jenis']) == (rekod['slug'], rekod['gaya'], rekod['jenis']): a['pilihan'] = False
        rekod['pilihan'] = pilihan; rekod.setdefault('tarikh', datetime.now().isoformat(timespec='seconds'))
        M['ambilan'].append(rekod); tulis(p, M)
    return rekod


def pilih(p, fail):
    """jadikan satu ambilan (laluan dalam bank) pilihan bagi (slug, gaya, jenis)nya"""
    p = _p(p)
    with _kunci:
        M = baca(p); sasar = next(a for a in M['ambilan'] if a['fail'] == fail)
        for a in M['ambilan']:
            if (a['slug'], a['gaya'], a['jenis']) == (sasar['slug'], sasar['gaya'], sasar['jenis']): a['pilihan'] = a is sasar
        tulis(p, M)


def ambilan_seterusnya(p, slug_, gaya, jenis):
    n = [a['ambilan'] for a in baca(p)['ambilan'] if (a['slug'], a['gaya'], a['jenis']) == (slug_, gaya, jenis)]
    return max(n, default=0) + 1


# ── klip rujukan ─────────────────────────────────────────────────────────────
def _kaya_istilah(teks):
    return sum(1 for p, _ in corak() if p.search(teks))


def rujukan(p, gaya):
    """(laluan klip, keterangan) untuk persona p. Susunan:
    gaya/<gaya>.json -> klip terbaik bank (8–12 s) -> gabungan ambilan ayat terbaik ~10 s -> rujukan/<gaya>.flac -> rujukan/santai.flac.
    Tidak pernah meminjam suara persona lain."""
    p = _p(p)
    f = p.gaya / f'{gaya}.json'
    if f.exists():
        g = json.load(open(f, encoding='utf-8'))
        if g.get('rujukan'):
            for asas in (p.dir, D):
                q = (asas / g['rujukan']).resolve()
                if q.exists() and q.is_relative_to(p.dir): return q, f'{p.nama}, tetap: {g["rujukan"]}'
    calon = [a for a in baca(p)['ambilan'] if a['gaya'] == gaya and a['jenis'] == 'ayat' and (a.get('skor_whisper') or 0) >= 0.9
             and not a.get('amaran') and (p.bank / a['fail']).exists()]
    nilai = lambda a: a['skor_whisper'] + 0.05 * _kaya_istilah(a['teks'])
    tepat = sorted([a for a in calon if 8 <= a['tempoh'] <= 12], key=nilai, reverse=True)
    if tepat: return p.bank / tepat[0]['fail'], f'{p.nama}, bank: {tepat[0]["fail"]}'
    if calon:
        dipilih, jum = [], 0.0
        for a in sorted(calon, key=nilai, reverse=True):
            if jum >= 9: break
            dipilih.append(a); jum += a['tempoh'] + 0.3
        if jum >= 6: return _gabung(p, gaya, dipilih), f'{p.nama}, gabungan {len(dipilih)} ambilan bank ({jum:.0f} s)'
    for n in (gaya, 'santai'):
        q = p.rujukan / f'{n}.flac'
        if q.exists(): return q, f'{p.nama}, lalai: rujukan/{n}.flac'
    if gaya != 'santai' and calon == []:
        try:
            return rujukan(p, 'santai')
        except SystemExit:
            pass
    raise SystemExit(f'Persona "{p.nama}" belum ada klip rujukan. Rakam sekurang-kurangnya 5 ayat yang bagus: '
                     f'bin/suara rakam --persona {p.nama}')


def _gabung(p, gaya, dipilih):
    import numpy as np, soundfile as sf
    KERJA.mkdir(exist_ok=True); out = KERJA / f'rujukan-{p.nama}-{gaya}.flac'
    bahagian = []
    for a in dipilih:
        y, sr = sf.read(p.bank / a['fail'], dtype='float32'); bahagian += [y, np.zeros(int(0.3 * sr), np.float32)]
    sf.write(out, np.concatenate(bahagian[:-1]), sr); return out
