"""Jana suara: `jana` (kontrak v1, video-template/docs/kontrak-suara.md) dan `cakap` (guna pantas macam edge-tts)."""
import json, re, sys, time
from pathlib import Path
import os, shutil
from . import VERSI, WHISPER_MODEL
from .sebutan import tukar
from .dengar import whisper, skor_terbaik
from .bank import rujukan

MIN_SKOR = 0.85


def log(*a):
    print(*a, file=sys.stderr, flush=True)


class Enjin:
    def __init__(self, gaya='santai', istilah=None):
        import torch
        from .model import muat
        self.torch = torch; self.gaya = gaya; self.istilah = istilah
        t0 = time.time(); self.m = muat()
        self.ruj, self.ket = rujukan(gaya)
        self.m.prepare_conditionals(str(self.ruj), exaggeration=0.5)
        self.boleh_semak = bool(shutil.which('whisper-cli')) and os.path.exists(WHISPER_MODEL)
        if not self.boleh_semak: log('  (whisper-cli atau modelnya tiada: semakan dan cuba semula dimatikan)')
        log(f'  suara-saya {VERSI}: model dimuat {time.time() - t0:.0f} s, gaya {gaya} ({self.ket})')

    @property
    def sr(self):
        return self.m.sr

    def satu(self, teks, benih=7, lang='ms', cuba=3, semak=True):
        """jana satu ayat; semak dengan whisper dan cuba semula dengan benih lain. Pulang (wav, teks_dihantar, skor, didengar, benih)"""
        dihantar = tukar(teks, self.istilah); terbaik = None; semak = semak and self.boleh_semak
        for k in range(cuba if semak else 1):
            b = int(benih) + 1000 * k
            self.torch.manual_seed(b)
            w = self.m.generate(dihantar, language_id=lang, cfg_weight=0.5, exaggeration=0.5, temperature=0.7).squeeze(0).numpy()
            if not semak: return w, dihantar, None, None, b
            import tempfile, soundfile as sf, os
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f: sf.write(f.name, w, self.sr)
            h = whisper(f.name, lang); os.remove(f.name)
            s = skor_terbaik(h, teks, dihantar)
            if terbaik is None or s > terbaik[2]: terbaik = (w, dihantar, s, h, b)
            if s >= MIN_SKOR: break
            log(f'    skor {s:.0%} (benih {b}), cuba semula: "{h}"')
        return terbaik


def jana(masuk, keluar):
    import numpy as np, soundfile as sf
    J = json.load(open(masuk, encoding='utf-8'))
    if J.get('kontrak', 1) != 1: sys.exit(f'Kontrak {J.get("kontrak")} tidak disokong (enjin ini: 1)')
    out = Path(keluar); out.mkdir(parents=True, exist_ok=True)
    gaya = J.get('gaya') or 'santai'; lang = J.get('bahasa', 'ms')
    E = Enjin(gaya, J.get('istilah')); res = []
    for a in J['ayat']:
        t0 = time.time()
        w, dihantar, s, h, b = E.satu(a['teks'], a.get('benih', 7), lang)
        sf.write(out / f"{a['id']}.wav", w.astype(np.float32), E.sr)
        res.append(dict(id=a['id'], fail=f"{a['id']}.wav", teks_dihantar=dihantar, skor_whisper=s, didengar=h, benih=b))
        log(f"  {a['id']}: {len(w) / E.sr:.1f} s audio, {time.time() - t0:.0f} s, " + (f'skor {s:.0%} ' if s is not None else '') + f"| {dihantar}")
    json.dump(dict(enjin=dict(nama='suara-saya', versi=VERSI, model='chatterbox-multilingual-v3', gaya=gaya, rujukan=E.ket), ayat=res),
              open(out / 'hasil.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def pecah_ayat(t):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', t) if s.strip()]


def cakap(teks, gaya, keluar, benih=7, semak=True, istilah=None):
    import numpy as np, soundfile as sf, subprocess
    if teks == '-': teks = sys.stdin.read()
    E = Enjin(gaya, istilah); bahagian = []; jeda = np.zeros(int(0.35 * E.sr), np.float32)
    for s in pecah_ayat(teks):
        w, dihantar, sk, h, b = E.satu(s, benih, semak=semak)
        bahagian += [w.astype(np.float32), jeda]
        log(f'  {len(w) / E.sr:.1f} s' + (f', skor {sk:.0%}' if sk is not None else '') + f' | {dihantar}')
    y = np.concatenate(bahagian[:-1]); y = y / max(1e-6, np.abs(y).max()) * 0.89
    keluar = Path(keluar)
    if keluar.suffix.lower() in ('.wav', '.flac'):
        sf.write(keluar, y, E.sr)
    else:      # .mp3/.m4a/... melalui ffmpeg
        tmp = keluar.with_suffix('.tmp.wav'); sf.write(tmp, y, E.sr)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp), str(keluar)], check=True); tmp.unlink()
    log(f'  -> {keluar} ({len(y) / E.sr:.1f} s)')
