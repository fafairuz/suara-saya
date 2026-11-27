"""Perakam bank suara: halaman web di 127.0.0.1 sahaja. Audio PCM mentah dari pelayar -> 48 kHz mono FLAC,
potong senyap, semak aras, semak whisper, skor. Ambilan lama tak pernah dipadam."""
import csv, json, re, shutil, subprocess, threading, uuid, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import numpy as np, soundfile as sf
from . import D, KERJA, ISTILAH
from .bank import slug, baca, tambah, ambilan_seterusnya, pilih
from .persona import dapat, senarai as senarai_persona, lalai as persona_lalai, cipta, PERSONA, ATURAN
from .dengar import whisper, skor_terbaik
from .sebutan import tukar

SR = 48000
DRAF = KERJA / 'draf'
GAYA_ASAS = ['santai', 'tegas', 'tanya']
_cache = {}


# ── senarai item ─────────────────────────────────────────────────────────────
def item(fail):
    p = Path(fail).expanduser().resolve()
    k = (str(p), p.stat().st_mtime)
    if k in _cache: return _cache[k]
    out = []
    if p.suffix.lower() == '.csv':
        ayat_dah = set()                   # ayat contoh yang dikongsi beberapa istilah dirakam sekali sahaja
        for r in csv.DictReader(open(p, encoding='utf-8')):
            ist = r['istilah'].strip(); s = slug(ist); seb = r.get('sebutan', '').strip()
            base = dict(istilah=ist, slug=s, sebutan=seb, contoh=r.get('contoh_ayat', '').strip(), maksud=r.get('maksud_bm', '').strip(),
                        jenis_istilah=r.get('jenis', ''))
            out.append(dict(base, jenis='kata', teks=r.get('bentuk_tulisan') or ist))
            if base['contoh'] and base['contoh'] not in ayat_dah:
                ayat_dah.add(base['contoh']); out.append(dict(base, jenis='ayat', teks=base['contoh']))
    else:
        baris = open(p, encoding='utf-8').read().splitlines()
        if p.suffix.lower() == '.md':      # baris bernombor, kecuali di bawah tajuk "Arahan ..."
            out_md, tajuk = [], ''
            for b in baris:
                if b.startswith('#'): tajuk = b.lower(); continue
                if 'arahan' in tajuk: continue
                if m := re.match(r'^\s*\d+[.)]\s+(.+)$', b): out_md.append(re.sub(r'[*_`]', '', m.group(1)).strip())
            baris = out_md
        else:
            baris = [b.strip().lstrip('-* ').strip() for b in baris if b.strip() and not b.lstrip().startswith('#')]
        for i, t in enumerate(baris, 1):
            out.append(dict(istilah=t, slug=f'{slug(p.stem)}-{i:03d}', sebutan='', contoh='', maksud='', jenis_istilah='', jenis='ayat', teks=t))
    _cache.clear(); _cache[k] = out
    return out


def status(fail, gaya, persona=None):
    P = dapat(persona); its = [dict(i) for i in item(fail)]; A = baca(P)['ambilan']
    ada = {}
    for a in A:
        if a['gaya'] == gaya: ada.setdefault((a['slug'], a['jenis']), []).append(a)
    for i in its:
        tk = ada.get((i['slug'], i['jenis']), [])
        if i['jenis'] == 'ayat': tk = [a for a in tk if a['teks'] == i['teks']]   # istilah sama dalam CSV lain, ayat lain
        i['ambilan'] = [dict(fail=a['fail'], url=P.rel(P.bank / a['fail']), ambilan=a['ambilan'], skor=a.get('skor_whisper'), pilihan=a.get('pilihan'), tempoh=a['tempoh'])
                        for a in tk]
        i['siap'] = any(a.get('pilihan') for a in tk)
    istilah = {}
    for i in its: istilah.setdefault(i['slug'], []).append(i['siap'])
    siap = sum(all(v) for v in istilah.values())
    return dict(item=its, kemajuan=dict(siap=siap, jumlah=len(istilah), item_siap=sum(i['siap'] for i in its), item_jumlah=len(its),
                                         label=f'{P.nama}: {siap}/{len(istilah)} {"istilah" if Path(fail).suffix == ".csv" else "ayat"}, gaya {gaya}'))


def senarai_gaya(persona=None):
    P = dapat(persona)
    g = set(GAYA_ASAS) | {f.stem for f in P.gaya.glob('*.json')} | {a['gaya'] for a in baca(P)['ambilan']}
    return GAYA_ASAS + sorted(g - set(GAYA_ASAS))


def senarai_fail():
    f = [ISTILAH] + sorted(p for p in D.glob('*') if p != ISTILAH and (p.suffix == '.csv' or (p.suffix in ('.md', '.txt') and p.stem.lower().startswith('skrip'))))
    f += sorted((D / 'skrip').glob('*')) if (D / 'skrip').exists() else []
    return [str(p) for p in f if p.exists()]


# ── proses rakaman ───────────────────────────────────────────────────────────
def db(x):
    return 20 * np.log10(max(float(x), 1e-9))


def proses(pcm, sr_masuk, teks, rujukan_lain=()):
    x = np.frombuffer(pcm, dtype=np.float32).astype(np.float64)
    if sr_masuk != SR:
        from scipy.signal import resample_poly
        from math import gcd
        g = gcd(SR, sr_masuk); x = resample_poly(x, SR // g, sr_masuk // g)
    amaran = []
    klip = int(np.sum(np.abs(x) >= 0.99))
    # potong senyap: tenaga setiap 10 ms
    n = int(0.01 * SR); fr = x[: len(x) // n * n].reshape(-1, n) if len(x) >= n else x.reshape(1, -1)
    e = 20 * np.log10(np.sqrt(np.mean(fr ** 2, axis=1)) + 1e-9)
    lantai = float(np.percentile(e, 10)); ambang = max(lantai + 12, -55)
    aktif = np.where(e > ambang)[0]
    if len(aktif) == 0:
        y = x; amaran.append('tiada suara dikesan')
    else:
        a = max(0, aktif[0] * n - int(0.15 * SR)); b = min(len(x), (aktif[-1] + 1) * n + int(0.25 * SR)); y = x[a:b].copy()
        f = int(0.01 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    tempoh = len(y) / SR
    puncak = db(np.max(np.abs(y))) if len(y) else -120
    rms = float(np.mean(e[aktif])) if len(aktif) else -120
    if klip > 3: amaran.append(f'clipping ({klip} sampel): perlahankan gain atau jauhkan sedikit mikrofon')
    elif puncak > -1: amaran.append('terlalu kuat (puncak > -1 dBFS)')
    if rms < -38 or puncak < -20: amaran.append('terlalu perlahan: dekatkan mikrofon atau naikkan gain')
    if lantai > -50: amaran.append(f'bunyi latar tinggi ({lantai:.0f} dBFS): matikan kipas/aircond')
    if tempoh < 0.3: amaran.append('terlalu pendek')
    DRAF.mkdir(parents=True, exist_ok=True)
    d = uuid.uuid4().hex[:12]; f = DRAF / f'{d}.flac'
    sf.write(f, y.astype(np.float32), SR, subtype='PCM_16')
    didengar = whisper(f)
    sk = skor_terbaik(didengar, teks, *rujukan_lain)
    if sk < 0.8: amaran.append(f'whisper dengar lain ({sk:.0%}): semak sebutan, atau rakam semula')
    return dict(draf=d, tempoh=round(tempoh, 2), puncak_db=round(puncak, 1), rms_db=round(rms, 1), lantai_db=round(lantai, 1),
                skor_whisper=sk, didengar=didengar, amaran=amaran)


# ── pelayan ──────────────────────────────────────────────────────────────────
class H(BaseHTTPRequestHandler):
    fail_lalai = str(ISTILAH)
    persona_lalai = None

    def log_message(self, *a): pass

    def hantar(self, kod, badan, jenis='application/json'):
        if not isinstance(badan, (bytes, bytearray)): badan = json.dumps(badan, ensure_ascii=False).encode()
        self.send_response(kod); self.send_header('Content-Type', jenis); self.send_header('Content-Length', str(len(badan)))
        self.send_header('Cache-Control', 'no-store'); self.end_headers(); self.wfile.write(badan)

    def q(self):
        u = urlparse(self.path); return u.path, {k: v[0] for k, v in parse_qs(u.query).items()}

    def do_GET(self):
        p, q = self.q()
        try:
            if p == '/uji':
                return self.hantar(200, (Path(__file__).parent / 'uji.html').read_bytes(), 'text/html; charset=utf-8')
            if p == '/api/uji/mula':
                from . import uji; return self.hantar(200, uji.mula(q.get('persona') or self.persona_lalai))
            if p == '/api/uji/rawak':
                from . import uji; return self.hantar(200, dict(teks=uji.ayat_rawak(q.get('mod', 'ayat'))))
            if p == '/api/uji/sebut':
                from . import uji; return self.hantar(200, uji.sebut(q.get('teks', '')))
            if p == '/':
                return self.hantar(200, (Path(__file__).parent / 'rakam.html').read_bytes(), 'text/html; charset=utf-8')
            if p == '/api/mula':
                pl = q.get('persona') or self.persona_lalai or persona_lalai()
                return self.hantar(200, dict(fail=senarai_fail(), fail_lalai=self.fail_lalai, gaya=senarai_gaya(pl), persona=senarai_persona(),
                                             persona_lalai=pl, aturan_persona=ATURAN))
            if p == '/api/item':
                return self.hantar(200, status(q.get('fail', self.fail_lalai), q.get('gaya', 'santai'), q.get('persona')))
            if p == '/audio':
                f = (D / q['f']).resolve()
                if not (f.is_relative_to(PERSONA) or f.is_relative_to(DRAF) or f.is_relative_to(KERJA / 'uji')) or not f.exists(): return self.hantar(404, {'ralat': 'tiada'})
                return self.hantar(200, f.read_bytes(), 'audio/flac')
            self.hantar(404, {'ralat': 'tiada'})
        except Exception as e:
            self.hantar(500, {'ralat': str(e)})

    def do_POST(self):
        p, q = self.q()
        badan = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        try:
            if p == '/api/rakaman':
                it = item(q['fail'])[int(q['indeks'])]
                lain = [tukar(it['teks'])]
                if it['jenis'] == 'kata':      # satu perkataan: whisper boleh tulis bentuk istilah atau ikut bunyi
                    lain += [it['istilah']] + ([it['sebutan'].replace('-', ''), it['sebutan'].replace('-', ' ')] if it['sebutan'] else [])
                return self.hantar(200, proses(badan, int(q['sr']), it['teks'], lain))
            if p == '/api/simpan':
                J = json.loads(badan); it = item(J['fail'])[int(J['indeks'])]; g = slug(J['gaya']) or 'santai'; P = dapat(J.get('persona'))
                src = DRAF / f"{re.sub(r'[^0-9a-f]', '', J['draf'])}.flac"
                n = ambilan_seterusnya(P, it['slug'], g, it['jenis'])
                rel = f"{it['slug']}/{g}-{it['jenis']}-{n:02d}.flac"; (P.bank / it['slug']).mkdir(parents=True, exist_ok=True)
                shutil.move(src, P.bank / rel)
                m = J.get('meta', {})
                rek = tambah(P, dict(fail=rel, istilah=it['istilah'], slug=it['slug'], teks=it['teks'], gaya=g, jenis=it['jenis'], ambilan=n,
                                  tempoh=m.get('tempoh'), skor_whisper=m.get('skor_whisper'), didengar=m.get('didengar'),
                                  puncak_db=m.get('puncak_db'), rms_db=m.get('rms_db'), amaran=m.get('amaran', []),
                                  sumber=Path(J['fail']).name))
                return self.hantar(200, rek)
            if p == '/api/pilih':
                J = json.loads(badan); pilih(J.get('persona'), J['fail'])
                return self.hantar(200, {'ok': True})
            if p == '/api/uji/jana':
                from . import uji; return self.hantar(200, uji.jana(json.loads(badan)))
            if p == '/api/uji/nilai':
                from . import uji; return self.hantar(200, uji.nilai(json.loads(badan)))
            if p == '/api/gaya':
                J = json.loads(badan); n = slug(J['nama']); P = dapat(J.get('persona'))
                if not n: return self.hantar(400, {'ralat': 'nama kosong'})
                P.gaya.mkdir(parents=True, exist_ok=True); f = P.gaya / f'{n}.json'
                if not f.exists(): f.write_text(json.dumps(dict(nama=n, rujukan=None), indent=1))
                return self.hantar(200, dict(gaya=senarai_gaya(P.nama), baru=n))
            if p == '/api/persona':
                J = json.loads(badan)
                try:
                    P = cipta((J.get('nama') or '').strip(), (J.get('paparan') or '').strip(), (J.get('keterangan') or '').strip(), bool(J.get('izin')))
                except ValueError as e:
                    return self.hantar(400, {'ralat': str(e)})
                return self.hantar(200, dict(persona=senarai_persona(), baru=P.nama))
            self.hantar(404, {'ralat': 'tiada'})
        except Exception as e:
            import traceback; traceback.print_exc()
            self.hantar(500, {'ralat': str(e)})


def jalan(port, fail, buka=True, persona=None):
    H.fail_lalai = str(Path(fail).resolve())
    if persona: H.persona_lalai = dapat(persona).nama
    s = ThreadingHTTPServer(('127.0.0.1', port), H)
    url = f'http://127.0.0.1:{port}/'
    print(f'Perakam suara-saya: {url}   portal uji: {url}uji   (localhost sahaja; Ctrl-C untuk henti)', flush=True)
    if buka: threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        pass
